from flask import Flask, request, jsonify, send_from_directory, abort, Response, current_app
from flask_migrate import Migrate
from models import db, Element, Category, ElementCharacteristic, AnalysisLog
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask_cors import CORS
from sqlalchemy import func
from flask_socketio import SocketIO, emit

import re
from config import SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER, ALLOWED_EXTENSIONS
from searching_alogrithm import get_dict

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# Конфигурация для загрузки файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

days_translation = {
    'Mon': 'Пн',
    'Tue': 'Вт',
    'Wed': 'Ср',
    'Thu': 'Чт',
    'Fri': 'Пт',
    'Sat': 'Сб',
    'Sun': 'Вс'
}

CHARACTERISTICS_MAPPING = {
    'energy_value': 'Энергетическая ценность',
    'sodium': 'Натрий',
    'total_sugar': 'Общий сахар',
    'free_sugars': 'Свободные сахара',
    'total_protein': 'Общий белок',
    'total_fat': 'Общее количество жиров',
    'fruit_content': 'Содержание фруктов',
    'age_marking': 'Возрастная маркировка',
    'high_sugar_front_packaging': 'Указание высокого содержания сахара',
}

@app.route('/api/images/<filename>')
def get_image(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    except FileNotFoundError:
        abort(404)

@app.route('/api/history')
def get_history():
    elements = Element.query.all()
    history_data = [get_element_data_by_id(element.id) for element in elements]
    return jsonify(history_data)

def get_element_data_by_id(element_id):
    element = Element.query.get(element_id)
    if not element:
        return None 

    category = Category.query.get(element.category_id)
    element_data = {
        "name": element.name,
        "imageUrl": element.file_name,
        "category": element.category.name if element.category else "N/A",
        "manufacturer": element.manufacturer,
        "date": element.analysis_date_time.strftime("%d-%m-%Y"),
        "status": "good", 
        "characteristics": []
    }

    for char in element.characteristics:
        for char_attr, char_name in CHARACTERISTICS_MAPPING.items():
            char_value = getattr(char, char_attr, 'N/A')
            
            status, min_value, max_value = determine_status(category, char_attr, char_value)
            characteristic_data = {
                "name": char_name,
                "value": char_value if char_value is not None else 'N/A',
                "status": status
            }
            
            if status == 'bad':
                characteristic_data["range"] = f"{min_value} - {max_value}"

            element_data["characteristics"].append(characteristic_data)

        labeling_value = "Выполнены" if not char.labeling else "Не выполнены"
        element_data["characteristics"].append({
            "name": "Требования к маркировке",
            "value": labeling_value,
            "status": "good" if not char.labeling else "bad"
        })

    element_data['status'] = determine_element_status(element_data["characteristics"])

    element.status = element_data['status']
    db.session.commit()

    return element_data

def determine_status(category, char_attr, char_value):
    min_value = getattr(category, f"{char_attr}_min", None)
    max_value = getattr(category, f"{char_attr}_max", None)
    if char_value is None:
        return 'N/A', None, None
    if min_value is not None and max_value is not None:
        if min_value <= char_value <= max_value:
            return 'good', min_value, max_value
        else:
            return 'bad', min_value, max_value
    return 'good', None, None

def determine_element_status(characteristics):
    element_status = 'good'

    for char in characteristics:
        if char['status'] == 'bad':
            element_status = 'bad'
            break 
        elif char['status'] == 'normal':
            element_status = 'normal'

    return element_status

@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    log_entry = AnalysisLog(message="Загрузка файла")
    db.session.add(log_entry)
    db.session.commit()

    filename = str.replace(file.filename, ' ', '_')
    file_path = f"{app.config['UPLOAD_FOLDER']}/{filename}"
    file.save(file_path)

    log_entry = AnalysisLog(message="Начало анализа изображения")
    db.session.add(log_entry)
    db.session.commit()

    analyse_data = get_dict(file_path)

    log_entry = AnalysisLog(message="Начало сохранения данных")
    db.session.add(log_entry)
    db.session.commit()

    id = save_element_data(analyse_data, filename)

    element = get_element_data_by_id(id)

    log_entry = AnalysisLog(message="Анализ завершен для файла" + analyse_data["name"])
    db.session.add(log_entry)
    db.session.commit()

    return jsonify({"message": "Image uploaded and analysis started", "data": element}), 200

def save_element_data(struct, path):
    new_element = Element(
        name=struct["name"] if struct["name"] != "N/A" else None,
        manufacturer=struct["manufacturer"] if struct["manufacturer"] != "N/A" else None,
        category_id=int(struct["category_id"]) if struct["category_id"] != "N/A" else None,
        description=struct["description"] if struct["description"] != "N/A" else None,
        analysis_date_time=datetime.utcnow() + timedelta(hours=2),
        file_name=path,
        status="Pending"
    )
    db.session.add(new_element)
    db.session.flush()

    new_characteristic = ElementCharacteristic(
        element_id=new_element.id,
        energy_value=float(str.replace(struct["characteristics"]["energy_value"], ',', '.')) if struct["characteristics"]["energy_value"] != "N/A" else None,
        sodium=float(str.replace(struct["characteristics"]["sodium"], ',', '.')) if struct["characteristics"]["sodium"] != "N/A" else None,
        total_sugar=float(str.replace(struct["characteristics"]["total_sugar"], ',', '.')) if struct["characteristics"]["total_sugar"] != "N/A" else None,
        free_sugars=float(str.replace(struct["characteristics"]["free_sugar"], ',', '.')) if struct["characteristics"]["free_sugar"] != "N/A" else None,
        total_protein=float(str.replace(struct["characteristics"]["total_protein"], ',', '.')) if struct["characteristics"]["total_protein"] != "N/A" else None,
        total_fat=float(str.replace(struct["characteristics"]["total_fat"], ',', '.')) if struct["characteristics"]["total_fat"] != "N/A" else None,
        fruit_content=float(str.replace(struct["characteristics"]["fruit_content"], ',', '.')) if struct["characteristics"]["fruit_content"] != "N/A" else None,
        age_marking=float(str.replace(struct["characteristics"]["age_marking"], ',', '.')) if struct["characteristics"]["age_marking"] != "N/A" else None,
        high_sugar_front_packaging=float(str.replace(struct["characteristics"]["high_sugar_front_packaging"], ',', '.')) if struct["characteristics"]["high_sugar_front_packaging"] != "N/A" else None,
        labeling=True if struct["characteristics"]["labeling"] == "Соответствует" else False
    )
    db.session.add(new_characteristic)
    db.session.commit()

    return new_element.id

def categoryData():
    categories_data = [
    {
        "name": "Сухие каши и крахмалистые продукты",
        "energy_value_min": 80,
        "energy_value_max": 100,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": None,
        "total_sugar_max": None,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": 0,
        "total_protein_max": 5.5,
        "total_fat_min": 0,
        "total_fat_max": 4.5,
        "fruit_content_min": 0,
        "fruit_content_max": 10,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": 30,
        "high_sugar_front_packaging_max": 100,
        "labeling_requirements": False
    },
    {
        "name": "Молочные продукты",
        "energy_value_min": 60,
        "energy_value_max": 100,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": None,
        "total_sugar_max": None,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": None,
        "total_protein_max": None,
        "total_fat_min": 0,
        "total_fat_max": 4.5,
        "fruit_content_min": 0,
        "fruit_content_max": 5,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": 40,
        "high_sugar_front_packaging_max": 100,
        "labeling_requirements": False
    },
    {
        "name": "Фруктовые и овощные пюре/коктейли",
        "energy_value_min": 60,
        "energy_value_max": 100,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": None,
        "total_sugar_max": None,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": None,
        "total_protein_max": None,
        "total_fat_min": 0,
        "total_fat_max": 4.5,
        "fruit_content_min": None,
        "fruit_content_max": None,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": 30,
        "high_sugar_front_packaging_max": 100,
        "labeling_requirements": False
    },
    {
        "name": "Фруктовые десерты",
        "energy_value_min": 0,
        "energy_value_max": 25,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": None,
        "total_sugar_max": None,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": None,
        "total_protein_max": None,
        "total_fat_min": 0,
        "total_fat_max": 4.5,
        "fruit_content_min": None,
        "fruit_content_max": None,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": 30,
        "high_sugar_front_packaging_max": 100,
        "labeling_requirements": False
    },
    {
        "name": "Поликомпонентные продукты/блюда",
        "energy_value_min": 60,
        "energy_value_max": 100,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": 0,
        "total_sugar_max": 15,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": 3,
        "total_protein_max": 100,
        "total_fat_min": 0,
        "total_fat_max": 4.5,
        "fruit_content_min": 0,
        "fruit_content_max": 5,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": None,
        "high_sugar_front_packaging_max": None,
        "labeling_requirements": False
    },
    {
        "name": "Сухие закуски",
        "energy_value_min": 0,
        "energy_value_max": 50,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": None,
        "total_sugar_max": None,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": None,
        "total_protein_max": None,
        "total_fat_min": 0,
        "total_fat_max": 4.5,
        "fruit_content_min": 100,
        "fruit_content_max": 100,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": 30,
        "high_sugar_front_packaging_max": 100,
        "labeling_requirements": False
    },
    {
        "name": "Перекусы",
        "energy_value_min": 0,
        "energy_value_max": 50,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": 0,
        "total_sugar_max": 15,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": 0,
        "total_protein_max": 5.5,
        "total_fat_min": 0,
        "total_fat_max": 4.5,
        "fruit_content_min": None,
        "fruit_content_max": None,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": None,
        "high_sugar_front_packaging_max": None,
        "labeling_requirements": False
    },
    {
        "name": "Ингредиенты",
        "energy_value_min": None,
        "energy_value_max": None,
        "sodium_min": 0,
        "sodium_max": 50,
        "total_sugar_min": None,
        "total_sugar_max": None,
        "free_sugars_min": None,
        "free_sugars_max": None,
        "total_protein_min": None,
        "total_protein_max": None,
        "total_fat_min": None,
        "total_fat_max": None,
        "fruit_content_min": None,
        "fruit_content_max": None,
        "age_marking_min": 6,
        "age_marking_max": 36,
        "high_sugar_front_packaging_min": None,
        "high_sugar_front_packaging_max": None,
        "labeling_requirements": False
    }]

        # Добавляем данные в базу данных
    for cat_data in categories_data:
        category = Category(**cat_data)
        db.session.add(category)

    db.session.commit()  # Фиксируем изменения

# Роут для отображения количества обработанных записей за сегодня
@app.route('/api/all', methods=['GET'])
def get_all_records_count():
    count = Element.query.filter(Element.analysis_date_time >= datetime.now() - timedelta(days=1)).count()
    return jsonify({'count': count})

# Роут для отображения количества частично рекомендуемых элементов
@app.route('/api/partially_recommended', methods=['GET'])
def get_cameras_count():
    count = Element.query.filter(Element.status == 'normal', Element.analysis_date_time >= datetime.now() - timedelta(days=1)).count()
    return jsonify({'count': count})

# Роут для отображения количества рекомендуемых элементов
@app.route('/api/recomended', methods=['GET'])
def get_detected_count():
    count = Element.query.filter(Element.status == 'good', Element.analysis_date_time >= datetime.now() - timedelta(days=1)).count()
    return jsonify({'count': count})

# Роут для отображения количества не рекомендуемых элементов за последний день
@app.route('/api/not_recomended', methods=['GET'])
def get_detected_fail_count():
    count = Element.query.filter(Element.status == 'bad', Element.analysis_date_time >= datetime.now() - timedelta(days=1)).count()
    return jsonify({'count': count})

# Роут для вывода количества обработанных записей за неделю
@app.route('/api/chart/elements', methods=['GET'])
def get_cameras_chart_data():
    
    cameras_data = (
        db.session.query(func.count(Element.id).label('count'), func.date_trunc('day', Element.analysis_date_time).label('day'))
        .filter(Element.analysis_date_time >= datetime.now() - timedelta(days=7))
        .group_by('day')
        .all()
    )

    cameras_dict = {days_translation[day[1].strftime("%a")]: day[0] for day in cameras_data}

    labels = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    data = [cameras_dict.get(day, 0) for day in labels]

    return jsonify({
        'labels': labels,
        'datasets': {'label': 'Количество обработанных записей', 'data': data}
    })

# Роут для вывода количества рекомендуемых товаров за неделю
@app.route('/api/chart/recomended', methods=['GET'])
def get_detected_chart_data():

    detected_data = (
        db.session.query(func.count(Element.id).label('count'), func.date_trunc('day', Element.analysis_date_time).label('day'))
        .filter(Element.analysis_date_time >= datetime.now() - timedelta(days=7), Element.status == 'good')
        .group_by('day')
        .all()
    )

    detected_dict = {days_translation[day[1].strftime("%a")]: day[0] for day in detected_data}

    labels = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    data = [detected_dict.get(day, 0) for day in labels]

    return jsonify({
        'labels': labels,
        'datasets': {'label': 'Количество рекомендуемых товаров', 'data': data}
    })

# Роут для вывода количества не рекомендуемых товаров за неделю
@app.route('/api/chart/not_recomended', methods=['GET'])
def get_detected_fail_chart_data():

    detected_fail_data = (
        db.session.query(func.count(Element.id).label('count'), func.date_trunc('day', Element.analysis_date_time).label('day'))
        .filter(Element.analysis_date_time >= datetime.now() - timedelta(days=7), Element.status == 'bad')
        .group_by('day')
        .all()
    )

    detected_fail_dict = {days_translation[day[1].strftime("%a")]: day[0] for day in detected_fail_data}

    labels = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
    data = [detected_fail_dict.get(day, 0) for day in labels]

    return jsonify({
        'labels': labels,
        'datasets': {'label': 'Количество не рекомендуемых товаров', 'data': data}
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='127.0.0.1', port=5000)