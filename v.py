import sys
import psycopg2
from PyQt5.QtWidgets import (QApplication, QWidget, QTableWidget,
                             QTableWidgetItem, QVBoxLayout, QLabel,
                             QLineEdit, QPushButton, QMessageBox,
                             QFormLayout, QHeaderView, QDialog,
                             QDialogButtonBox, QComboBox, QDateTimeEdit, QGridLayout)
from PyQt5.QtCore import Qt, QDate

# Параметры подключения к базе данных (замените на свои)
DATABASE = {
    "host": "localhost",
    "database": "test",
    "user": "postgres",
    "password": "postgres",
    "options": "-c client_encoding=UTF8"
}

# Цветовая палитра
DARK_BACKGROUND = "#282C34"
WHITE_TEXT = "#FFFFFF"
DARK_PURPLE_BORDER = "#663399"

# ================== ФОРМА АВТОРИЗАЦИИ ==================
class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Авторизация')
        self.setGeometry(200, 200, 300, 150)

        self.initUI()

    def initUI(self):
        self.loginLabel = QLabel("Логин:")
        self.loginEdit = QLineEdit()
        self.passwordLabel = QLabel("Пароль:")
        self.passwordEdit = QLineEdit()
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.loginButton = QPushButton("Войти")
        self.loginButton.clicked.connect(self.checkLogin)
        self.cancelButton = QPushButton("Отмена")
        self.cancelButton.clicked.connect(self.reject)

        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
        """)

        layout = QVBoxLayout()
        layout.addWidget(self.loginLabel)
        layout.addWidget(self.loginEdit)
        layout.addWidget(self.passwordLabel)
        layout.addWidget(self.passwordEdit)
        layout.addWidget(self.loginButton)
        layout.addWidget(self.cancelButton)
        self.setLayout(layout)

    def checkLogin(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()

        if login == "" and password == "":
            self.accept()
        else:
            QMessageBox.warning(self, 'Ошибка', 'Неверный логин или пароль')

# ================== ГЛАВНОЕ ОКНО ==================
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Управление базой данных "ИнтерТех"')
        self.setGeometry(100, 100, 400, 300)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 10px;
                margin: 5px; /* Добавили отступы между кнопками */
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
        """)

        grid = QGridLayout()
        grid.setSpacing(10)  # Устанавливаем промежуток между кнопками

        # Создаем кнопки (оставляем только основные)
        self.customersButton = QPushButton("Клиенты")
        self.warehousesButton = QPushButton("Склады")
        self.suppliersButton = QPushButton("Поставщики")
        self.productsButton = QPushButton("Товары")
        self.ordersButton = QPushButton("Заказы")
        self.employeesButton = QPushButton("Сотрудники")
        self.stockButton = QPushButton("Остатки")

        # Добавляем кнопки в сетку
        grid.addWidget(self.customersButton, 0, 0)  # Строка 0, Колонка 0
        grid.addWidget(self.warehousesButton, 0, 1)  # Строка 0, Колонка 1
        grid.addWidget(self.suppliersButton, 0, 2)  # Строка 0, Колонка 2
        grid.addWidget(self.productsButton, 1, 0)  # Строка 1, Колонка 0
        grid.addWidget(self.ordersButton, 1, 1)  # Строка 1, Колонка 1
        grid.addWidget(self.employeesButton, 1, 2)  # Строка 1, Колонка 2
        grid.addWidget(self.stockButton, 2, 0)  # Строка 2, Колонка 0

        # Создаем кнопки для второй сетки
        self.orderDetailsButton = QPushButton("Состав заказа")
        self.searchButton = QPushButton("Найти по имени/телефону")
        self.createOrderButton = QPushButton("Оформить заказ")
        self.orderFromSupplierButton = QPushButton("Заказать у поставщика")

        # Создаем отдельный layout для второй сетки
        grid2 = QGridLayout()
        grid2.setSpacing(10)
        grid2.addWidget(self.orderDetailsButton, 0, 0)
        grid2.addWidget(self.searchButton, 0, 1)
        grid2.addWidget(self.createOrderButton, 1, 0)
        grid2.addWidget(self.orderFromSupplierButton, 1, 1)

        # Добавляем кнопку "Выход"
        self.exitButton = QPushButton("Выход")
        self.exitButton.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #8B0000; /* Темно-бордовый цвет */
                    }}
                    QPushButton:hover {{
                        background-color: #B22222; /* Немного светлее при наведении */
                    }}
                """)
        self.exitButton.clicked.connect(QApplication.instance().quit)

        # Добавляем отступы между кнопками и краями окна
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(grid)
        mainLayout.addSpacing(20)  # Добавляем отступ между сетками
        mainLayout.addLayout(grid2)
        mainLayout.addSpacing(20)
        mainLayout.addWidget(self.exitButton)  # Добавляем кнопку выхода
        mainLayout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(mainLayout)

        # Подключаем сигналы к слотам (для новых кнопок)
        self.orderDetailsButton.clicked.connect(self.showOrderDetailsForm)
        self.searchButton.clicked.connect(self.showSearchForm)
        self.createOrderButton.clicked.connect(self.showCreateOrderForm)
        self.orderFromSupplierButton.clicked.connect(self.showOrderFromSupplierForm)

        # старые подключения
        self.customersButton.clicked.connect(self.showCustomersForm)
        self.warehousesButton.clicked.connect(self.showWarehousesForm)
        self.suppliersButton.clicked.connect(self.showSuppliersForm)
        self.productsButton.clicked.connect(self.showProductsForm)
        self.ordersButton.clicked.connect(self.showOrdersForm)
        self.employeesButton.clicked.connect(self.showEmployeesForm)
        self.stockButton.clicked.connect(self.showStockForm)
        self.orderDetailsButton.clicked.connect(self.showOrderDetailsForm)

    def showCustomersForm(self):
        self.customersForm = CustomersForm()
        self.customersForm.show()

    def showWarehousesForm(self):
        self.warehousesForm = WarehousesForm()
        self.warehousesForm.show()

    def showSuppliersForm(self):
        self.suppliersForm = SuppliersForm()
        self.suppliersForm.show()

    def showProductsForm(self):
        self.productsForm = ProductsForm()
        self.productsForm.show()

    def showOrdersForm(self):
        self.ordersForm = OrdersForm()
        self.ordersForm.show()

    def showEmployeesForm(self):
        self.employeesForm = EmployeesForm()
        self.employeesForm.show()

    def showStockForm(self):
        self.stockForm = StockForm()
        self.stockForm.show()

    def showOrderDetailsForm(self):
        self.orderDetailsForm = OrderDetailsForm()
        self.orderDetailsForm.show()

    def showSearchForm(self):
        self.searchForm = SearchForm()
        self.searchForm.show()

    def showCreateOrderForm(self):
        self.createOrderForm = CreateOrderForm()
        self.createOrderForm.show()

    def showOrderFromSupplierForm(self):
        QMessageBox.information(self, "Заглушка", "Форма заказа у поставщика будет реализована позже")

# ================== ФОРМА "КЛИЕНТЫ" ==================
class CustomersForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Клиенты')
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Тип", "Имя", "Адрес", "Телефон", "Email", "ИНН"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.addButton = QPushButton("Добавить")
        self.editButton = QPushButton("Изменить")
        self.deleteButton = QPushButton("Удалить")

        self.addButton.clicked.connect(self.addCustomer)
        self.editButton.clicked.connect(self.editCustomer)
        self.deleteButton.clicked.connect(self.deleteCustomer)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Customers")
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def addCustomer(self):
        form = AddEditCustomerForm(self)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def editCustomer(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите клиента для редактирования')
            return

        customer_id = self.tableWidget.item(row, 0).text()
        form = AddEditCustomerForm(self, customer_id)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def deleteCustomer(self):
      row = self.tableWidget.currentRow()
      if row < 0:
          QMessageBox.warning(self, 'Ошибка', 'Выберите клиента для удаления')
          return

      customer_id = self.tableWidget.item(row, 0).text()

      reply = QMessageBox.question(self, 'Удалить', 'Вы уверены, что хотите удалить клиента?',
                                  QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
      if reply == QMessageBox.Yes:
          try:
              conn = psycopg2.connect(**DATABASE)
              cursor = conn.cursor()
              cursor.execute("DELETE FROM Customers WHERE Customer_ID = %s", (customer_id,))
              conn.commit()
              cursor.close()
              conn.close()
              self.loadData()
          except Exception as e:
              QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить клиента: {e}')

class AddEditCustomerForm(QDialog):
    def __init__(self, parent=None, customer_id=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать клиента')
        self.customer_id = customer_id

        self.initUI()
        if customer_id:
            self.loadData()

    def initUI(self):
        self.customerTypeLabel = QLabel("Тип клиента:")
        self.customerTypeEdit = QLineEdit()
        self.customerNameLabel = QLabel("Имя клиента:")
        self.customerNameEdit = QLineEdit()
        self.addressLabel = QLabel("Адрес:")
        self.addressEdit = QLineEdit()
        self.phoneLabel = QLabel("Телефон:")
        self.phoneEdit = QLineEdit()
        self.emailLabel = QLabel("Email:")
        self.emailEdit = QLineEdit()
        self.innLabel = QLabel("ИНН:")
        self.innEdit = QLineEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        formLayout = QFormLayout()
        formLayout.addRow(self.customerTypeLabel, self.customerTypeEdit)
        formLayout.addRow(self.customerNameLabel, self.customerNameEdit)
        formLayout.addRow(self.addressLabel, self.addressEdit)
        formLayout.addRow(self.phoneLabel, self.phoneEdit)
        formLayout.addRow(self.emailLabel, self.emailEdit)
        formLayout.addRow(self.innLabel, self.innEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def loadData(self):
      try:
          conn = psycopg2.connect(**DATABASE)
          cursor = conn.cursor()
          cursor.execute("SELECT CustomerType, Customer_Name, Address, Phone, Email, INN FROM Customers WHERE Customer_ID = %s", (self.customer_id,))
          row = cursor.fetchone()

          if row:
            self.customerTypeEdit.setText(row[0])
            self.customerNameEdit.setText(row[1])
            self.addressEdit.setText(row[2])
            self.phoneEdit.setText(row[3])
            self.emailEdit.setText(row[4])
            self.innEdit.setText(row[5])

          cursor.close()
          conn.close()
      except Exception as e:
          QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def accept(self):
        customer_type = self.customerTypeEdit.text()
        customer_name = self.customerNameEdit.text()
        address = self.addressEdit.text()
        phone = self.phoneEdit.text()
        email = self.emailEdit.text()
        inn = self.innEdit.text()

        if not customer_type or not customer_name:
            QMessageBox.warning(self, 'Ошибка', 'Поля "Тип клиента" и "Имя клиента" обязательны для заполнения')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            if self.customer_id:
                # Редактирование существующего клиента
                cursor.execute("""
                    UPDATE Customers
                    SET CustomerType = %s, Customer_Name = %s, Address = %s, Phone = %s, Email = %s, INN = %s
                    WHERE Customer_ID = %s
                """, (customer_type, customer_name, address, phone, email, inn, self.customer_id))
            else:
                # Добавление нового клиента
                cursor.execute("""
                    INSERT INTO Customers (CustomerType, Customer_Name, Address, Phone, Email, INN)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (customer_type, customer_name, address, phone, email, inn))

            conn.commit()
            cursor.close()
            conn.close()
            super().accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {e}')

# ================== ФОРМА "СОСТАВ ЗАКАЗА" ==================
class OrderDetailsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Состав заказа')
        self.setGeometry(100, 100, 800, 400)

        self.initUI()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.orderIdLabel = QLabel("ID заказа:")
        self.orderIdEdit = QLineEdit()
        self.loadButton = QPushButton("Загрузить")
        self.loadButton.clicked.connect(self.loadOrderDetails)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название товара", "Количество", "Цена", "Сумма", "ФИО клиента", "ФИО сотрудника"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeToContents)

        formLayout = QFormLayout()
        formLayout.addRow(self.orderIdLabel, self.orderIdEdit)
        formLayout.addRow(self.loadButton)

        self.layout = QVBoxLayout()
        self.layout.addLayout(formLayout)
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

    def loadOrderDetails(self):
        order_id = self.orderIdEdit.text()
        if not order_id:
            QMessageBox.warning(self, 'Внимание', 'Введите ID заказа')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT
                    o.Order_ID,
                    p.pName AS ProductName,
                    o.Quantity,
                    o.Price,
                    o.Quantity * o.Price AS TotalPrice,
                    c.Customer_Name,
                    e.Employee_Name
                FROM
                    Orders o
                JOIN
                    Customers c ON o.Customer_ID = c.Customer_ID
                JOIN
                    Products p ON o.Product_ID = p.Product_ID
                JOIN
                    Employees e ON o.Employee_ID = e.Employee_ID
                WHERE
                    o.Order_ID = %s
            """, (order_id,))

            rows = cursor.fetchall()

            if not rows:
                QMessageBox.information(self, 'Информация', 'Заказ с таким ID не найден')
                return

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable) # Запрет редактирования
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

# ================== ФОРМА "СКЛАДЫ" ==================
class WarehousesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Склады')
        self.setGeometry(200, 200, 600, 400)
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Адрес"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.addButton = QPushButton("Добавить")
        self.editButton = QPushButton("Изменить")
        self.deleteButton = QPushButton("Удалить")

        self.addButton.clicked.connect(self.addWarehouse)
        self.editButton.clicked.connect(self.editWarehouse)
        self.deleteButton.clicked.connect(self.deleteWarehouse)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Warehouses")
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def addWarehouse(self):
        form = AddEditWarehouseForm(self)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def editWarehouse(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите склад для редактирования')
            return

        warehouse_id = self.tableWidget.item(row, 0).text()
        form = AddEditWarehouseForm(self, warehouse_id)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def deleteWarehouse(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите склад для удаления')
            return

        warehouse_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, 'Удалить', 'Вы уверены, что хотите удалить склад?',
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = psycopg2.connect(**DATABASE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Warehouses WHERE Warehouse_ID = %s", (warehouse_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.loadData()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить склад: {e}')

class AddEditWarehouseForm(QDialog):
    def __init__(self, parent=None, warehouse_id=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать склад')
        self.warehouse_id = warehouse_id

        self.initUI()
        if warehouse_id:
            self.loadData()

    def initUI(self):
        self.warehouseNameLabel = QLabel("Название склада:")
        self.warehouseNameEdit = QLineEdit()
        self.warehouseAddressLabel = QLabel("Адрес склада:")
        self.warehouseAddressEdit = QLineEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        formLayout = QFormLayout()
        formLayout.addRow(self.warehouseNameLabel, self.warehouseNameEdit)
        formLayout.addRow(self.warehouseAddressLabel, self.warehouseAddressEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT Warehouse_Name, Warehouse_Address FROM Warehouses WHERE Warehouse_ID = %s", (self.warehouse_id,))
            row = cursor.fetchone()

            if row:
                self.warehouseNameEdit.setText(row[0])
                self.warehouseAddressEdit.setText(row[1])

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def accept(self):
        warehouse_name = self.warehouseNameEdit.text()
        warehouse_address = self.warehouseAddressEdit.text()

        if not warehouse_name or not warehouse_address:
            QMessageBox.warning(self, 'Ошибка', 'Поля "Название склада" и "Адрес склада" обязательны для заполнения')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            if self.warehouse_id:
                # Редактирование существующего склада
                cursor.execute("""
                    UPDATE Warehouses
                    SET Warehouse_Name = %s, Warehouse_Address = %s
                    WHERE Warehouse_ID = %s
                """, (warehouse_name, warehouse_address, self.warehouse_id))
            else:
                # Добавление нового склада
                cursor.execute("""
                    INSERT INTO Warehouses (Warehouse_Name, Warehouse_Address)
                    VALUES (%s, %s)
                """, (warehouse_name, warehouse_address))

            conn.commit()
            cursor.close()
            conn.close()
            super().accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {e}')

# ================== ФОРМА "ПОСТАВЩИКИ" ==================
class SuppliersForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Поставщики')
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Название", "Адрес", "Телефон", "Email", "ИНН", "Контактное лицо"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.addButton = QPushButton("Добавить")
        self.editButton = QPushButton("Изменить")
        self.deleteButton = QPushButton("Удалить")

        self.addButton.clicked.connect(self.addSupplier)
        self.editButton.clicked.connect(self.editSupplier)
        self.deleteButton.clicked.connect(self.deleteSupplier)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Suppliers")
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def addSupplier(self):
        form = AddEditSupplierForm(self)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def editSupplier(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите поставщика для редактирования')
            return

        supplier_id = self.tableWidget.item(row, 0).text()
        form = AddEditSupplierForm(self, supplier_id)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def deleteSupplier(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите поставщика для удаления')
            return

        supplier_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, 'Удалить', 'Вы уверены, что хотите удалить поставщика?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = psycopg2.connect(**DATABASE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Suppliers WHERE Supplier_ID = %s", (supplier_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.loadData()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить поставщика: {e}')

class AddEditSupplierForm(QDialog):
    def __init__(self, parent=None, supplier_id=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать поставщика')
        self.supplier_id = supplier_id

        self.initUI()
        if supplier_id:
            self.loadData()

    def initUI(self):
        self.supplierNameLabel = QLabel("Название поставщика:")
        self.supplierNameEdit = QLineEdit()
        self.addressLabel = QLabel("Адрес:")
        self.addressEdit = QLineEdit()
        self.phoneLabel = QLabel("Телефон:")
        self.phoneEdit = QLineEdit()
        self.emailLabel = QLabel("Email:")
        self.emailEdit = QLineEdit()
        self.innLabel = QLabel("ИНН:")
        self.innEdit = QLineEdit()
        self.contactPersonLabel = QLabel("Контактное лицо:")
        self.contactPersonEdit = QLineEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        formLayout = QFormLayout()
        formLayout.addRow(self.supplierNameLabel, self.supplierNameEdit)
        formLayout.addRow(self.addressLabel, self.addressEdit)
        formLayout.addRow(self.phoneLabel, self.phoneEdit)
        formLayout.addRow(self.emailLabel, self.emailEdit)
        formLayout.addRow(self.innLabel, self.innEdit)
        formLayout.addRow(self.contactPersonLabel, self.contactPersonEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Supplier_Name, Address, Phone, Email, INN, Contact_Person FROM Suppliers WHERE Supplier_ID = %s",
                (self.supplier_id,))
            row = cursor.fetchone()

            if row:
                self.supplierNameEdit.setText(row[0])
                self.addressEdit.setText(row[1])
                self.phoneEdit.setText(row[2])
                self.emailEdit.setText(row[3])
                self.innEdit.setText(row[4])
                self.contactPersonEdit.setText(row[5])

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def accept(self):
        supplier_name = self.supplierNameEdit.text()
        address = self.addressEdit.text()
        phone = self.phoneEdit.text()
        email = self.emailEdit.text()
        inn = self.innEdit.text()
        contact_person = self.contactPersonEdit.text()

        if not supplier_name:
            QMessageBox.warning(self, 'Ошибка', 'Поле "Название поставщика" обязательно для заполнения')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            if self.supplier_id:
                # Редактирование существующего поставщика
                cursor.execute("""
                            UPDATE Suppliers
                            SET Supplier_Name = %s, Address = %s, Phone = %s, Email = %s, INN = %s, Contact_Person = %s
                            WHERE Supplier_ID = %s
                        """, (supplier_name, address, phone, email, inn, contact_person, self.supplier_id))
            else:
                # Добавление нового поставщика
                cursor.execute("""
                            INSERT INTO Suppliers (Supplier_Name, Address, Phone, Email, INN, Contact_Person)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """, (supplier_name, address, phone, email, inn, contact_person))

            conn.commit()
            cursor.close()
            conn.close()
            super().accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {e}')

# ================== ФОРМА "ТОВАРЫ" ==================
class ProductsForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Товары')
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Название", "Описание", "Артикул", "Категория", "Цена закупки", "Цена продажи", "Ед. измерения"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.addButton = QPushButton("Добавить")
        self.editButton = QPushButton("Изменить")
        self.deleteButton = QPushButton("Удалить")

        self.addButton.clicked.connect(self.addProduct)
        self.editButton.clicked.connect(self.editProduct)
        self.deleteButton.clicked.connect(self.deleteProduct)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT Product_ID, pName, Description, VendorCode, Category, Purchase_Price, Selling_Price, Unit FROM Products")
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def addProduct(self):
        form = AddEditProductForm(self)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def editProduct(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите товар для редактирования')
            return

        product_id = self.tableWidget.item(row, 0).text()
        form = AddEditProductForm(self, product_id)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def deleteProduct(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите товар для удаления')
            return

        product_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, 'Удалить', 'Вы уверены, что хотите удалить товар?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = psycopg2.connect(**DATABASE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Products WHERE Product_ID = %s", (product_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.loadData()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить товар: {e}')

class AddEditProductForm(QDialog):
    def __init__(self, parent=None, product_id=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать товар')
        self.product_id = product_id

        self.initUI()
        if product_id:
            self.loadData()

    def initUI(self):
        self.productNameLabel = QLabel("Название товара:")
        self.productNameEdit = QLineEdit()
        self.descriptionLabel = QLabel("Описание:")
        self.descriptionEdit = QLineEdit()
        self.vendorCodeLabel = QLabel("Артикул:")
        self.vendorCodeEdit = QLineEdit()
        self.categoryLabel = QLabel("Категория:")
        self.categoryEdit = QLineEdit()
        self.purchasePriceLabel = QLabel("Цена закупки:")
        self.purchasePriceEdit = QLineEdit()
        self.sellingPriceLabel = QLabel("Цена продажи:")
        self.sellingPriceEdit = QLineEdit()
        self.unitLabel = QLabel("Единица измерения:")
        self.unitEdit = QLineEdit()
        self.supplierNameLabel = QLabel("Поставщик:")
        self.supplierNameEdit = QLineEdit()
        self.supplierIdEdit = QLineEdit()
        # self.supplierIdEdit.setReadOnly(True)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        formLayout = QFormLayout()
        formLayout.addRow(self.productNameLabel, self.productNameEdit)
        formLayout.addRow(self.descriptionLabel, self.descriptionEdit)
        formLayout.addRow(self.vendorCodeLabel, self.vendorCodeEdit)
        formLayout.addRow(self.categoryLabel, self.categoryEdit)
        formLayout.addRow(self.purchasePriceLabel, self.purchasePriceEdit)
        formLayout.addRow(self.sellingPriceLabel, self.sellingPriceEdit)
        formLayout.addRow(self.unitLabel, self.unitEdit)
        formLayout.addRow(self.supplierNameLabel, self.supplierNameEdit)
        formLayout.addRow(self.supplierIdEdit, self.supplierIdEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT pName, Description, VendorCode, Category, Purchase_Price, Selling_Price, Unit, Supplier_ID FROM Products WHERE Product_ID = %s",
                (self.product_id,))
            row = cursor.fetchone()

            if row:
                self.productNameEdit.setText(row[0])
                self.descriptionEdit.setText(row[1])
                self.vendorCodeEdit.setText(row[2])
                self.categoryEdit.setText(row[3])
                self.purchasePriceEdit.setText(str(row[4]))
                self.sellingPriceEdit.setText(str(row[5]))
                self.unitEdit.setText(row[6])
                cursor.execute("SELECT Supplier_Name FROM Suppliers WHERE Supplier_ID = %s", (row[7],))
                supplier_name = cursor.fetchone()[0]
                self.supplierNameEdit.setText(supplier_name)
                self.supplierIdEdit.setText(str(row[7]))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def accept(self):
        product_name = self.productNameEdit.text()
        description = self.descriptionEdit.text()
        vendor_code = self.vendorCodeEdit.text()
        category = self.categoryEdit.text()
        purchase_price = self.purchasePriceEdit.text()
        selling_price = self.sellingPriceEdit.text()
        unit = self.unitEdit.text()
        supplier_name = self.supplierNameEdit.text()

        if not product_name or not category:
            QMessageBox.warning(self, 'Ошибка', 'Поля "Название товара" и "Категория" обязательны для заполнения')
            return

        try:
            purchase_price = float(purchase_price)
            selling_price = float(selling_price)
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Цены должны быть числовыми значениями')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT Supplier_ID FROM Suppliers WHERE Supplier_Name = %s", (supplier_name,))
            supplier_row = cursor.fetchone()
            if supplier_row:
                supplier_id = supplier_row[0]
            else:
                QMessageBox.warning(self, 'Ошибка', f'Поставщик "{supplier_name}" не найден')
                return

            if self.product_id:
                # Редактирование существующего товара
                cursor.execute("""
                    UPDATE Products
                    SET pName = %s, Description = %s, VendorCode = %s, Category = %s, Purchase_Price = %s, Selling_Price = %s, Unit = %s, Supplier_ID = %s
                    WHERE Product_ID = %s
                """, (
                product_name, description, vendor_code, category, purchase_price, selling_price, unit, supplier_id,
                self.product_id))
            else:
                # Добавление нового товара
                cursor.execute("""
                    INSERT INTO Products (pName, Description, VendorCode, Category, Purchase_Price, Selling_Price, Unit, Supplier_ID)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                product_name, description, vendor_code, category, purchase_price, selling_price, unit, supplier_id))

            conn.commit()
            cursor.close()
            conn.close()
            super().accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {e}')

# ================== ФОРМА "ЗАКАЗЫ" ==================
class OrdersForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Заказы')
        self.setGeometry(200, 200, 800, 600)
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(
            ["ID", "Клиент", "Дата", "Сумма", "Статус", "Сотрудник", "ID товара", "Количество", "Цена"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.addButton = QPushButton("Добавить")
        self.editButton = QPushButton("Изменить")
        self.deleteButton = QPushButton("Удалить")

        self.addButton.clicked.connect(self.addOrder)
        self.editButton.clicked.connect(self.editOrder)
        self.deleteButton.clicked.connect(self.deleteOrder)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT o.Order_ID, c.Customer_Name, o.Order_Date, o.Total_Amount, o.Order_Status, e.Employee_Name, o.Product_ID, o.Quantity, o.Price FROM Orders o JOIN Customers c ON o.Customer_ID = c.Customer_ID JOIN Employees e ON o.Employee_ID = e.Employee_ID")
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def addOrder(self):
        form = AddEditOrderForm(self)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def editOrder(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ для редактирования')
            return

        order_id = self.tableWidget.item(row, 0).text()
        form = AddEditOrderForm(self, order_id)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def deleteOrder(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите заказ для удаления')
            return

        order_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, 'Удалить', 'Вы уверены, что хотите удалить заказ?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = psycopg2.connect(**DATABASE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Orders WHERE Order_ID = %s", (order_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.loadData()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить заказ: {e}')

class AddEditOrderForm(QDialog):
    def __init__(self, parent=None, order_id=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать заказ')
        self.order_id = order_id

        self.initUI()
        if order_id:
            self.loadData()

    def initUI(self):
        self.customerNameLabel = QLabel("Клиент:")
        self.customerNameEdit = QLineEdit()
        self.customerIdEdit = QLineEdit()  # Скрытое поле для ID клиента
        self.orderDateLabel = QLabel("Дата заказа:")
        self.orderDateEdit = QLineEdit()
        self.totalAmountLabel = QLabel("Сумма заказа:")
        self.totalAmountEdit = QLineEdit()
        self.orderStatusLabel = QLabel("Статус заказа:")
        self.orderStatusEdit = QLineEdit()
        self.employeeNameLabel = QLabel("Сотрудник:")
        self.employeeNameEdit = QLineEdit()
        self.employeeIdEdit = QLineEdit()  # Скрытое поле для ID сотрудника
        self.commentLabel = QLabel("Комментарий:")
        self.commentEdit = QLineEdit()
        self.productNameLabel = QLabel("Товар:")
        self.productNameEdit = QLineEdit()
        self.productIdEdit = QLineEdit()  # Скрытое поле для ID товара
        self.quantityLabel = QLabel("Количество:")
        self.quantityEdit = QLineEdit()
        self.priceLabel = QLabel("Цена:")
        self.priceEdit = QLineEdit()

        self.customerIdEdit.setReadOnly(True)
        self.employeeIdEdit.setReadOnly(True)
        self.productIdEdit.setReadOnly(True)
        self.totalAmountEdit.setReadOnly(True)

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        formLayout = QFormLayout()
        formLayout.addRow(self.customerNameLabel, self.customerNameEdit)
        formLayout.addRow(self.customerIdEdit, self.customerIdEdit)
        formLayout.addRow(self.orderDateLabel, self.orderDateEdit)
        formLayout.addRow(self.totalAmountLabel, self.totalAmountEdit)
        formLayout.addRow(self.orderStatusLabel, self.orderStatusEdit)
        formLayout.addRow(self.employeeNameLabel, self.employeeNameEdit)
        formLayout.addRow(self.employeeIdEdit, self.employeeIdEdit)
        formLayout.addRow(self.commentLabel, self.commentEdit)
        formLayout.addRow(self.productNameLabel, self.productNameEdit)
        formLayout.addRow(self.productIdEdit, self.productIdEdit)
        formLayout.addRow(self.quantityLabel, self.quantityEdit)
        formLayout.addRow(self.priceLabel, self.priceEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT Customer_ID, Order_Date, Total_Amount, Order_Status, Employee_ID, Comment, Product_ID, Quantity, Price FROM Orders WHERE Order_ID = %s", (self.order_id,))
            order_row = cursor.fetchone()

            if order_row:
                customer_id = order_row[0]
                order_date = order_row[1]
                total_amount = order_row[2]
                order_status = order_row[3]
                employee_id = order_row[4]
                comment = order_row[5]
                product_id = order_row[6]
                quantity = order_row[7]
                price = order_row[8]

                cursor.execute("SELECT Customer_Name FROM Customers WHERE Customer_ID = %s", (customer_id,))
                customer_name = cursor.fetchone()
                if customer_name:
                    customer_name = customer_name[0]

                cursor.execute("SELECT Employee_Name FROM Employees WHERE Employee_ID = %s", (employee_id,))
                employee_name = cursor.fetchone()
                if employee_name:
                    employee_name = employee_name[0]

                cursor.execute("SELECT pName FROM Products WHERE Product_ID = %s", (product_id,))
                product_name = cursor.fetchone()
                if product_name:
                    product_name = product_name[0]

                self.customerNameEdit.setText(customer_name)
                self.customerIdEdit.setText(str(customer_id))
                self.orderDateEdit.setText(str(order_date))
                self.totalAmountEdit.setText(str(total_amount))
                self.orderStatusEdit.setText(order_status)
                self.employeeNameEdit.setText(employee_name)
                self.employeeIdEdit.setText(str(employee_id))
                self.commentEdit.setText(comment)
                self.productNameEdit.setText(product_name)
                self.productIdEdit.setText(str(product_id))
                self.quantityEdit.setText(str(quantity))
                self.priceEdit.setText(str(price))

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def accept(self):
        customer_name = self.customerNameEdit.text()
        order_date = self.orderDateEdit.text()
        total_amount = self.totalAmountEdit.text()
        order_status = self.orderStatusEdit.text()
        employee_name = self.employeeNameEdit.text()
        comment = self.commentEdit.text()
        product_name = self.productNameEdit.text()
        quantity = self.quantityEdit.text()
        price = self.priceEdit.text()

        if not all([customer_name, order_date, order_status, employee_name, product_name, quantity, price]):
            QMessageBox.warning(self, 'Ошибка', 'Необходимо заполнить поля: Клиент, Дата заказа, Статус заказа, Сотрудник, Товар, Количество, Цена')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            cursor.execute("SELECT Customer_ID FROM Customers WHERE Customer_Name = %s", (customer_name,))
            customer_row = cursor.fetchone()
            if customer_row:
                customer_id = customer_row[0]
            else:
                QMessageBox.warning(self, 'Ошибка', f'Клиент "{customer_name}" не найден')
                return

            cursor.execute("SELECT Employee_ID FROM Employees WHERE Employee_Name = %s", (employee_name,))
            employee_row = cursor.fetchone()
            if employee_row:
                employee_id = employee_row[0]
            else:
                QMessageBox.warning(self, 'Ошибка', f'Сотрудник "{employee_name}" не найден')
                return

            cursor.execute("SELECT Product_ID FROM Products WHERE pName = %s", (product_name,))
            product_row = cursor.fetchone()
            if product_row:
                product_id = product_row[0]
            else:
                QMessageBox.warning(self, 'Ошибка', f'Товар "{product_name}" не найден')
                return

            if self.order_id:
                # Редактирование существующего заказа
                cursor.execute("""
                    UPDATE Orders
                    SET Customer_ID = %s, Order_Date = %s, Total_Amount = %s, Order_Status = %s, Employee_ID = %s, Comment = %s, Product_ID = %s, Quantity = %s, Price = %s
                    WHERE Order_ID = %s
                """, (customer_id, order_date, total_amount, order_status, employee_id, comment, product_id, quantity, price, self.order_id))
            else:
                # Добавление нового заказа
                cursor.execute("""
                    INSERT INTO Orders (Customer_ID, Order_Date, Total_Amount, Order_Status, Employee_ID, Comment, Product_ID, Quantity, Price)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (customer_id, order_date, total_amount, order_status, employee_id, comment, product_id, quantity, price))

            conn.commit()
            cursor.close()
            conn.close()
            super().accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {e}')

# ================== ФОРМА "СОТРУДНИКИ" ==================
class EmployeesForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Сотрудники')
        self.setGeometry(200, 200, 800, 400)
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "ФИО", "Должность", "Телефон", "Email"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.addButton = QPushButton("Добавить")
        self.editButton = QPushButton("Изменить")
        self.deleteButton = QPushButton("Удалить")

        self.addButton.clicked.connect(self.addEmployee)
        self.editButton.clicked.connect(self.editEmployee)
        self.deleteButton.clicked.connect(self.deleteEmployee)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        layout.addWidget(self.addButton)
        layout.addWidget(self.editButton)
        layout.addWidget(self.deleteButton)
        self.setLayout(layout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Employees")
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def addEmployee(self):
        form = AddEditEmployeeForm(self)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def editEmployee(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудника для редактирования')
            return

        employee_id = self.tableWidget.item(row, 0).text()
        form = AddEditEmployeeForm(self, employee_id)
        if form.exec_() == QDialog.Accepted:
            self.loadData()

    def deleteEmployee(self):
        row = self.tableWidget.currentRow()
        if row < 0:
            QMessageBox.warning(self, 'Ошибка', 'Выберите сотрудника для удаления')
            return

        employee_id = self.tableWidget.item(row, 0).text()

        reply = QMessageBox.question(self, 'Удалить', 'Вы уверены, что хотите удалить сотрудника?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                conn = psycopg2.connect(**DATABASE)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Employees WHERE Employee_ID = %s", (employee_id,))
                conn.commit()
                cursor.close()
                conn.close()
                self.loadData()
            except Exception as e:
                QMessageBox.critical(self, 'Ошибка', f'Не удалось удалить сотрудника: {e}')

class AddEditEmployeeForm(QDialog):
    def __init__(self, parent=None, employee_id=None):
        super().__init__(parent)
        self.setWindowTitle('Добавить/Редактировать сотрудника')
        self.employee_id = employee_id

        self.initUI()
        if employee_id:
            self.loadData()

    def initUI(self):
        self.employeeNameLabel = QLabel("ФИО сотрудника:")
        self.employeeNameEdit = QLineEdit()
        self.positionLabel = QLabel("Должность:")
        self.positionEdit = QLineEdit()
        self.phoneLabel = QLabel("Телефон:")
        self.phoneEdit = QLineEdit()
        self.emailLabel = QLabel("Email:")
        self.emailEdit = QLineEdit()

        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        formLayout = QFormLayout()
        formLayout.addRow(self.employeeNameLabel, self.employeeNameEdit)
        formLayout.addRow(self.positionLabel, self.positionEdit)
        formLayout.addRow(self.phoneLabel, self.phoneEdit)
        formLayout.addRow(self.emailLabel, self.emailEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT Employee_Name, Position, Phone, Email FROM Employees WHERE Employee_ID = %s", (self.employee_id,))
            row = cursor.fetchone()

            if row:
                self.employeeNameEdit.setText(row[0])
                self.positionEdit.setText(row[1])
                self.phoneEdit.setText(row[2])
                self.emailEdit.setText(row[3])

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

    def accept(self):
        employee_name = self.employeeNameEdit.text()
        position = self.positionEdit.text()
        phone = self.phoneEdit.text()
        email = self.emailEdit.text()

        if not employee_name or not position:
            QMessageBox.warning(self, 'Ошибка', 'Поля "ФИО сотрудника" и "Должность" обязательны для заполнения')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            if self.employee_id:
                # Редактирование существующего сотрудника
                cursor.execute("""
                        UPDATE Employees
                        SET Employee_Name = %s, Position = %s, Phone = %s, Email = %s
                        WHERE Employee_ID = %s
                    """, (employee_name, position, phone, email, self.employee_id))
            else:
                # Добавление нового сотрудника
                cursor.execute("""
                        INSERT INTO Employees (Employee_Name, Position, Phone, Email)
                        VALUES (%s, %s, %s, %s)
                    """, (employee_name, position, phone, email))

            conn.commit()
            cursor.close()
            conn.close()
            super().accept()

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось сохранить данные: {e}')

# ================== ФОРМА "ОСТАТКИ" ==================
class StockForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Остатки')
        self.setGeometry(200, 200, 600, 400)
        self.initUI()
        self.loadData()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(3)  # ID Склада, Наименование товара, Количество
        self.tableWidget.setHorizontalHeaderLabels(["ID Склада", "Наименование товара", "Количество"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def loadData(self):
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT w.Warehouse_ID, p.pName, s.Quantity
                FROM Stock s
                JOIN Warehouses w ON s.Warehouse_ID = w.Warehouse_ID
                JOIN Products p ON s.Product_ID = p.Product_ID
            """)
            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить данные: {e}')

# ================== ФОРМА ПОИСКА ==================
class SearchForm(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Поиск')
        self.setGeometry(200, 200, 600, 400)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QTableWidget {{
                border: 2px solid {DARK_PURPLE_BORDER};
                gridline-color: {DARK_PURPLE_BORDER};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QHeaderView::section {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
                border: 1px solid {DARK_PURPLE_BORDER};
                padding: 4px;
            }}
        """)
        # Поля ввода
        self.searchLabel = QLabel("Поиск по имени/телефону:")
        self.searchEdit = QLineEdit()
        self.searchButton = QPushButton("Найти")
        self.searchButton.clicked.connect(self.search)

        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Тип", "Имя", "Адрес", "Телефон", "Email", "ИНН"])
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)

        formLayout = QFormLayout()
        formLayout.addRow(self.searchLabel, self.searchEdit)
        formLayout.addRow(self.searchButton)

        layout = QVBoxLayout()
        layout.addLayout(formLayout)
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)

    def search(self):
        search_text = self.searchEdit.text()

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT *
                FROM Customers
                WHERE Customer_Name ILIKE %s OR Phone ILIKE %s
            """, (f'%{search_text}%', f'%{search_text}%'))  # ILIKE регистронезависимый поиск

            rows = cursor.fetchall()

            self.tableWidget.setRowCount(len(rows))
            for i, row in enumerate(rows):
                for j, col in enumerate(row):
                    item = QTableWidgetItem(str(col))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Запрет редактирования
                    self.tableWidget.setItem(i, j, item)

            cursor.close()
            conn.close()

            if not rows:
                QMessageBox.information(self, 'Информация', 'По вашему запросу ничего не найдено')

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось выполнить поиск: {e}')

# ================== Форма создание заказа ==================
class CreateOrderForm(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Оформление заказа')
        self.setGeometry(200, 200, 400, 300)
        self.initUI()

    def initUI(self):
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QLineEdit {{
                border: 2px solid {DARK_PURPLE_BORDER};
            }}
            QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QPushButton:hover {{
                background-color: #7F52B3;
            }}
            QLabel {{
                color: {WHITE_TEXT};
            }}
            QMessageBox {{
                background-color: {DARK_BACKGROUND};
                color: {WHITE_TEXT};
            }}
            QMessageBox QPushButton {{
                background-color: {DARK_PURPLE_BORDER};
                border: none;
                padding: 5px;
            }}
            QComboBox {{
                border: 2px solid {DARK_PURPLE_BORDER};
                padding: 5px;
            }}
        """)
        self.customerLabel = QLabel("Клиент:")
        self.customerComboBox = QComboBox()
        self.loadCustomers()  # Загружаем клиентов в ComboBox
        self.customerComboBox.currentIndexChanged.connect(self.updateCustomerInfo)

        self.customerIdLabel = QLabel("ID Клиента:")
        self.customerIdEdit = QLineEdit()
        self.customerIdEdit.setReadOnly(True)

        self.orderDateLabel = QLabel("Дата заказа:")
        self.orderDateEdit = QDateTimeEdit(QDate.currentDate())
        self.orderDateEdit.setDisplayFormat("yyyy-MM-dd")
        self.orderDateEdit.setCalendarPopup(True)  # Добавляем календарь

        self.productLabel = QLabel("Товар:")
        self.productComboBox = QComboBox()
        self.loadProducts()  # Загружаем товары в ComboBox
        self.productComboBox.currentIndexChanged.connect(self.updateProductInfo)

        self.productIdLabel = QLabel("ID Товара:")
        self.productIdEdit = QLineEdit()
        self.productIdEdit.setReadOnly(True)

        self.quantityLabel = QLabel("Количество:")
        self.quantityEdit = QLineEdit()

        self.priceLabel = QLabel("Цена:")
        self.priceEdit = QLineEdit()
        self.priceEdit.setReadOnly(True)

        self.employeeLabel = QLabel("Сотрудник:")
        self.employeeComboBox = QComboBox()
        self.loadEmployees()  # Загружаем сотрудников в ComboBox
        self.employeeComboBox.currentIndexChanged.connect(self.updateEmployeeInfo)

        self.employeeIdLabel = QLabel("ID Сотрудника:")
        self.employeeIdEdit = QLineEdit()
        self.employeeIdEdit.setReadOnly(True)

        self.commentLabel = QLabel("Комментарий:")
        self.commentEdit = QLineEdit()

        self.addButton = QPushButton("Добавить заказ")
        self.addButton.clicked.connect(self.addOrder)

        self.addNewCustomerButton = QPushButton("Добавить нового клиента")
        self.addNewCustomerButton.clicked.connect(self.addNewCustomer)

        # Размещение на форме
        layout = QFormLayout()
        layout.addRow(self.customerLabel, self.customerComboBox)
        layout.addRow(self.customerIdLabel, self.customerIdEdit)
        layout.addRow(self.addNewCustomerButton)
        layout.addRow(self.orderDateLabel, self.orderDateEdit)
        layout.addRow(self.productLabel, self.productComboBox)
        layout.addRow(self.productIdLabel, self.productIdEdit)
        layout.addRow(self.quantityLabel, self.quantityEdit)
        layout.addRow(self.priceLabel, self.priceEdit)
        layout.addRow(self.employeeLabel, self.employeeComboBox)
        layout.addRow(self.employeeIdLabel, self.employeeIdEdit)
        layout.addRow(self.commentLabel, self.commentEdit)
        layout.addRow(self.addButton)
        self.setLayout(layout)

    def addNewCustomer(self):
        # Открываем форму для добавления нового клиента
        form = AddEditCustomerForm(self)
        if form.exec_() == QDialog.Accepted:
            QMessageBox.information(self, 'Успех', 'Новый клиент успешно добавлен')
            self.loadCustomers()  # Обновляем список клиентов
            # Устанавливаем в QComboBox только что добавленного клиента
            new_customer_name = form.customerNameEdit.text()  # Предполагаем, что у вас есть такое поле
            index = self.customerComboBox.findText(new_customer_name)
            if index >= 0:
                self.customerComboBox.setCurrentIndex(index)

    def loadCustomers(self):
        # Загрузка клиентов в QComboBox
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT Customer_ID, Customer_Name FROM Customers")
            customers = cursor.fetchall()
            cursor.close()
            conn.close()

            self.customerComboBox.clear()  # Сначала очищаем ComboBox

            for customer_id, customer_name in customers:
                self.customerComboBox.addItem(customer_name, customer_id)

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить клиентов: {e}')

    def updateCustomerInfo(self):
        # Обновление информации о клиенте при выборе из QComboBox
        selected_customer_id = self.customerComboBox.currentData()  # Получаем данные (ID клиента)
        if selected_customer_id:
            self.customerIdEdit.setText(str(selected_customer_id))
        else:
            self.customerIdEdit.clear()

    def loadProducts(self):
        # Загрузка товаров в QComboBox
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT Product_ID, pName FROM Products")
            products = cursor.fetchall()
            cursor.close()
            conn.close()

            for product_id, product_name in products:
                self.productComboBox.addItem(product_name, product_id)  # Используем addItem с двумя аргументами

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить товары: {e}')

    def updateProductInfo(self):
        # Обновление информации о товаре при выборе из QComboBox
        selected_product_id = self.productComboBox.currentData()  # Получаем данные (ID товара)
        if selected_product_id:
            self.productIdEdit.setText(str(selected_product_id))
            # Здесь также можно добавить обновление цены товара, если цена не фиксированная
        else:
            self.productIdEdit.clear()

    def loadEmployees(self):
        # Загрузка сотрудников в QComboBox
        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()
            cursor.execute("SELECT Employee_ID, Employee_Name FROM Employees")
            employees = cursor.fetchall()
            cursor.close()
            conn.close()

            for employee_id, employee_name in employees:
                self.employeeComboBox.addItem(employee_name, employee_id)  # Используем addItem с двумя аргументами

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось загрузить сотрудников: {e}')

    def updateEmployeeInfo(self):
        # Обновление информации о сотруднике при выборе из QComboBox
        selected_employee_id = self.employeeComboBox.currentData()  # Получаем данные (ID сотрудника)
        if selected_employee_id:
            self.employeeIdEdit.setText(str(selected_employee_id))
        else:
            self.employeeIdEdit.clear()

    def addOrder(self):
        # Получение данных из полей
        customer_id = self.customerIdEdit.text()
        order_date = self.orderDateEdit.dateTime().toString("yyyy-MM-dd")
        employee_id = self.employeeIdEdit.text()
        product_id = self.productIdEdit.text()
        quantity = self.quantityEdit.text()
        price = self.priceEdit.text()
        comment = self.commentEdit.text()
        order_status = 'Новый'  # Статус заказа

        # Проверка на пустые поля
        if not all([customer_id, order_date, employee_id, product_id, quantity, price]):
            QMessageBox.warning(self, 'Ошибка', 'Необходимо заполнить все поля!')
            return

        try:
            # Преобразование в числовые типы
            quantity = int(quantity)
            price = float(price)
            total_amount = float(quantity) * float(price)  # Расчет суммы
        except ValueError:
            QMessageBox.warning(self, 'Ошибка', 'Количество и цена должны быть числовыми значениями!')
            return

        try:
            conn = psycopg2.connect(**DATABASE)
            cursor = conn.cursor()

            # Вставка данных в таблицу Orders
            cursor.execute("""
                INSERT INTO Orders (Customer_ID, Order_Date, Total_Amount, Order_Status, Employee_ID, Comment, Product_ID, Quantity, Price)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            customer_id, order_date, total_amount, order_status, employee_id, comment, product_id, quantity, price))

            conn.commit()
            cursor.close()
            conn.close()

            QMessageBox.information(self, 'Успех', 'Заказ успешно добавлен')
            self.accept()  # Закрываем форму

        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Не удалось добавить заказ: {e}')



# ================== ГЛАВНАЯ ФУНКЦИЯ ==================
def main():
    app = QApplication(sys.argv)

    login_form = LoginForm()
    if login_form.exec_() == QDialog.Accepted:
        main_window = MainWindow()
        main_window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()