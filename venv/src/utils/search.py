from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt


def search(db_manager,root):
    text = root.line_edit_search.text()
    query= f"""
                SELECT id,pib,`rank`,`group`
                FROM kurs
                WHERE pib LIKE '{text}%';

                    """
    arr = db_manager.execute_query(query)
    if arr:


        x = arr[0][0]
        name = arr[0][1]

        rank = arr[0][2]
        group = arr[0][3]
        root.search_l.setText(f"{rank} {name} C-{group} Группа")
        query=f"""SELECT 
                `date`, 
                CASE 
                    WHEN {x} IN (dn1_id) THEN 'Дневальний'
                    WHEN {x} IN (dn2_id) THEN 'Дневальний'
                    WHEN {x}  IN (dng_id) THEN 'Дневальна'
                    WHEN {x} IN (chk_id) THEN 'Черговий'
                    WHEN {x} IN (chnk27_id) THEN 'Черговий27'
                    WHEN {x}  IN (pchnk271_id) THEN 'Помічник27'
                    WHEN {x}  IN (pchnk272_id) THEN 'Помічник27'
                    WHEN {x}  IN (pchnk273_id) THEN 'Помічник27'
                    WHEN {x}  IN (schp_id) THEN 'Старший ЧП'
                END AS column_name
            FROM 
                data_table
            WHERE 
                {x} IN (dn1_id, dn2_id, dng_id,chk_id,chnk27_id,pchnk271_id,pchnk272_id,pchnk273_id,schp_id)
    
    """
        print(query)
        x=db_manager.execute_query(query)
        print(x)

        root.container2 = QWidget()  # Создаем контейнер для виджетов
        root.layout2 = QVBoxLayout()  # Создаем вертикальное расположение для виджетов в контейнере
        root.layout2.setSpacing(0)  # Set the spacing between widgets to 0
        root.layout2.setAlignment(Qt.AlignTop)  # Align the layout to the top
        root.container2.setLayout(root.layout2)

        root.scroll_area.setWidget(root.container2)
        for date, label_text in x:
            text = f"{date}: {label_text}"  # Format the text
            label = QLabel(text)  # Create QLabel with the formatted text
            label.setFixedHeight(30)  # Set a fixed height for each QLabel (adjust the value as needed)
            root.layout2.addWidget(label)  # Add QLabel to the vertical layout

