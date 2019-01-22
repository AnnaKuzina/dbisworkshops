from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     SubmitField,
                     BooleanField,
                     SelectField,
                     IntegerField,
                     TextField,
                     FloatField,
                     validators)


class LoginForm(FlaskForm):
    login = StringField('Логін: ', validators=[
        validators.DataRequired('Введіть Ваш логін'),
        validators.Length(min=5, max=30, message='Допустима кількість символів для лігіна між 5 та 30')
    ])
    password = PasswordField('Пароль: ', validators=[
        validators.DataRequired('Введіть Ваш пароль')])
    remember_me = BooleanField('Запам\'ятати мене')
    submit = SubmitField('Увійти')


class RegistrationForm(FlaskForm):
    login = StringField('Логін:', validators=[
        validators.DataRequired('Введіть Ваш логін'),
        validators.Length(min=5, max=30, message='Допустима кількість символів для лігіна між 5 та 30')
    ])
    name = StringField('Ім\'я:', validators=[
        validators.DataRequired('Введіть Ваше Ім\'я'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в імені між 5 та 30')])
    password = PasswordField('Пароль:', validators=[
        validators.DataRequired('Введіть Ваш пароль'),
        validators.Length(min=5, max=30, message='Допустима кількість символів пароля між 5 та 30')])
    password_repeat = PasswordField('Повторіть пароль:', validators=[
        validators.DataRequired('Повторіть Ваш пароль'),
        validators.EqualTo('password', 'Паролі не співпадають')
    ])
    registration = SubmitField('Зареєструватися')


class AddGiftForm(FlaskForm):
    name = StringField('Назва подарунка', validators=[
        validators.DataRequired('Введіть назву подарунка'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в назві між 5 та 30')])
    price = FloatField('Вартість подарунка', validators=[
        validators.DataRequired('Введіть вартість подарунку'),
        validators.NumberRange(message='Доступна ціна товару - від 0 до 1000 у.о.', min=0, max=1000)])
    desc = StringField('Опис подарунка', validators=[validators.DataRequired('Введіть опис подарунка')])
    submit = SubmitField('Додати')


class AddFeatureForm(FlaskForm):
    name = StringField('Назва характеристрики', validators=[
        validators.DataRequired('Введіть назву характеристрики'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в назві між 5 та 30')])
    submit = SubmitField('Додати')


class AddCategoryForm(FlaskForm):
    name = StringField('Назва Категорії', validators=[
        validators.DataRequired('Введіть назву категорії'),
        validators.Length(min=5, max=30, message='Допустима кількість символів в назві між 5 та 30')])
    submit = SubmitField('Додати')


def create_update_gift_form(gift_names):
    class DynamicForm(FlaskForm):
        name = SelectField('Назва: ', choices=[(name, name) for name in gift_names])
    setattr(DynamicForm, 'price', FloatField('Вартість подарунка', validators=[
        validators.DataRequired('Введіть вартість подарунку'),
        validators.NumberRange(message='Доступна ціна товару - від 0 до 1000 у.о.', min=0, max=1000)]))
    setattr(DynamicForm, 'desc', StringField('Опис подарунка', validators=[
        validators.DataRequired('Введіть опис подарунка')]))
    setattr(DynamicForm, 'submit', SubmitField('Змінти'))
    return DynamicForm()


def create_select_form(keys):
    class DynamicForm(FlaskForm):
        name = SelectField('Назва: ', choices=[(key, key) for key in keys])
    setattr(DynamicForm, 'submit', SubmitField('Видалити'))
    return DynamicForm()


def create_select_relation_form(gift_keys, feature_keys):
    class DynamicForm(FlaskForm):
        gift_key = SelectField('Назва подарунка: ', choices=[(key, key) for key in gift_keys])
    for key in feature_keys:
        setattr(DynamicForm, key, BooleanField(key))
    setattr(DynamicForm, 'submit', SubmitField('Обрати'))
    return DynamicForm()


def create_select_feature_form(feature_list):
    class DynamicForm(FlaskForm):
        pass
    for key in feature_list:
        setattr(DynamicForm, key, BooleanField(key))
    setattr(DynamicForm, 'submit', SubmitField('Обрати'))
    return DynamicForm()

# class AddProductForm(FlaskForm):
#     name = StringField('Назва', validators=[
#         validators.DataRequired('Введіть назву товару'),
#         validators.Length(min=5, max=30, message='Допустима кількість символів в назві між 5 та 30')])
#     count = IntegerField('Кількість', validators=[
#         validators.NumberRange(message='Доступна кількість товару - від 0 до 1000', min=0, max=1000)
#     ])
#     submit = SubmitField('Додати товар')
#
#
# def create_update_product_form(product_names):
#     class DynamicForm(FlaskForm):
#         name = SelectField('Назва: ', choices=[(item, item) for item in product_names])
#     setattr(DynamicForm, 'count', IntegerField('Кількість', validators=[
#         validators.NumberRange(message='Доступна кількість товару - від 0 до 1000', min=0, max=1000)
#     ]))
#     setattr(DynamicForm, 'submit', SubmitField('Змінти'))
#     return DynamicForm()
#
#
# def create_select_form(items, label_submit='Обрати'):
#     class DynamicForm(FlaskForm):
#         name = SelectField('Назва: ', choices=[(item, item) for item in items])
#     setattr(DynamicForm, 'submit', SubmitField(label=label_submit))
#     return DynamicForm()
#
