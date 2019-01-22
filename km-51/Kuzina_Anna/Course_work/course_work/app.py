import datetime

from flask import Flask, session, request, render_template, url_for, redirect, make_response
import pandas as pd

from data_base import *
from forms import *

app = Flask(__name__)
app.secret_key = 'secret_key'

package_map = {
    'gift': GiftPackage(),
    'feature': FeaturePackage(),
    'category': CategoryPackage(),
    'gift_feature': GiftFeaturePackage(),
    'gift_category': GiftCategoryPackage()
}


@app.route('/')
def index():
    user_login = session.get('login') or request.cookies.get('login')
    return render_template('index.html', user_login=user_login) if user_login else redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserPackage()
        login_res = user.login(request.form['login'], request.form['password']).values[0, 0]
        if login_res:
            response = make_response(redirect('/'))
            session['login'] = request.form['login']
            if request.form.get('remember_me'):
                expires = datetime.datetime.now() + datetime.timedelta(days=10)
                response.set_cookie('login', request.form['login'], expires=expires)
            return response
        return render_template('authorization/login.html', form=form, problem='Невірний пароль або логін')
    return render_template('authorization/login.html', form=form)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = UserPackage()
        status = user.registration(request.form['login'], request.form['name'], request.form['password'])
        if status == 'ok':
            session['login'] = request.form['login']
            return redirect('/')
        problem = 'Користувач з таким логіном уже існує'
        problem = problem if status == problem else 'Перевірте коректність введення усіх полів'
        return render_template('authorization/registration.html', form=form, problem=problem)
    return render_template('authorization/registration.html', form=form)


@app.route('/logout')
def logout():
    response = make_response(redirect('/login'))
    response.set_cookie('login', '', expires=0)
    session['login'] = None
    return response


@app.route('/table/<table_name>')
def show_table(table_name):
    package = package_map[table_name]
    table = package.get_all()
    is_mutable = package.mutable
    return render_template('tables/show_table.html', table=table.to_html(), table_name=table_name,is_mutable=is_mutable)


@app.route('/table/gift/add', methods=['GET', 'POST'])
def add_gift():
    form = AddGiftForm()
    problem = None
    if form.validate_on_submit():
        package = package_map['gift']
        status = package.add(request.form['name'], request.form['price'], request.form['desc'])
        if status == 'ok':
            return redirect(url_for('show_table', table_name='gift'))
        problem = 'Такий подарунок уже існує'
        problem = problem if status == problem else 'Перевірте коректність введення усіх полів'
    return render_template('tables/add.html', table_name='gift', form=form, problem=problem)


@app.route('/table/feature/add', methods=['GET', 'POST'])
def add_feature():
    form = AddFeatureForm()
    problem = None
    if form.validate_on_submit():
        package = package_map['feature']
        status = package.add(request.form['name'])
        if status == 'ok':
            return redirect(url_for('show_table', table_name='feature'))
        problem = 'Така характеристика уже існує'
        problem = problem if status == problem else 'Перевірте коректність введення усіх полів'
    return render_template('tables/add.html', table_name='feature', form=form, problem=problem)


@app.route('/table/category/add', methods=['GET', 'POST'])
def add_category():
    form = AddCategoryForm()
    problem = None
    if form.validate_on_submit():
        package = package_map['category']
        status = package.add(request.form['name'])
        if status == 'ok':
            return redirect(url_for('show_table', table_name='category'))
        problem = 'Така характеристика уже існує'
        problem = problem if status == problem else 'Перевірте коректність введення усіх полів'
    return render_template('tables/add.html', table_name='category', form=form, problem=problem)


@app.route('/table/gift/update', methods=['GET', 'POST'])
def update_gift():
    package = package_map['gift']
    gift_names = package.get_keys()
    form = create_update_gift_form(gift_names)
    problem = None
    if form.validate_on_submit():
        status = package.update(request.form['name'], request.form['price'], request.form['desc'])
        if status == 'ok':
            return redirect(url_for('show_table', table_name='gift'))
        problem = 'Перевірте коректність введення усіх полів'
    return render_template('tables/update.html', table_name='gift', form=form, problem=problem)


@app.route('/table/<table_name>/delete', methods=['GET', 'POST'])
def delete_from_table(table_name):
    package = package_map[table_name]
    keys = package.get_keys()
    form = create_select_form(keys)
    problem = None
    if form.validate_on_submit():
        status = package.delete(request.form['name'])
        if status == 'ok':
            return redirect(url_for('show_table', table_name=table_name))
        problem = 'Перевірте коректність введення усіх полів'
    return render_template('tables/delete.html', problem=problem, table_name=table_name, form=form)


@app.route('/gift_feature')
def gift_feature():
    return render_template('gift/gift_feature.html')


@app.route('/gift_category')
def gift_category():
    return render_template('gift/gift_category.html')


@app.route('/<action>/select_gift', methods=['GET', 'POST'])
def select_gift(action):
    package = GiftPackage()
    gift_names_list = package.get_keys()
    form = create_select_form(gift_names_list)
    if form.validate_on_submit():
        package_main = package_map[action]
        feature_names_list = package_main.get_gift_list(request.form['name']).values[:, 0]

        return render_template('gift/all_gift_feature.html',
                               gift_name=request.form['name'],
                               feature_names_list=feature_names_list)
    return render_template('gift/select_gift.html', form=form)


@app.route('/select_gift_relation/<relation_name>', methods=['GET', 'POST'])
def select_gift_relation(relation_name):
    package1 = GiftPackage()
    package2 = package_map[relation_name]
    package_main = package_map['gift_' + relation_name]
    form = create_select_relation_form(package1.get_keys(), package2.get_keys())
    problem = None
    if form.validate_on_submit():
        gift_key = request.form['gift_key']
        bleak_list = ['gift_key', 'csrf_token', 'submit']
        keys_list = [line for line in request.form if line not in bleak_list]
        status = package_main.delete(gift_key)
        if status == 'ok':
            for key in keys_list:
                status = package_main.add(key, gift_key)
                if status != 'ok':
                    problem = 'Перевірте коректність введення усіх полів'
                    break
            else:
                return redirect(url_for('select_gift', action='gift_feature'))
    return render_template('gift/select_gift_relation.html', problem=problem, form=form, text='Характеристики: ')


@app.route('/make_advice', methods=['GET', 'POST'] )
def make_advice():
    package = GiftFeaturePackage()
    feature_keys = FeaturePackage().get_keys()
    form = create_select_feature_form(feature_keys)
    if form.validate_on_submit():
        bleak_list = ['csrf_token', 'submit']
        selected_features = [line for line in request.form if line not in bleak_list]
        advice_list = package.get_advice(selected_features)
        group_advice = pd.groupby(advice_list, 'GIFT_NAME').size()
        advice_list['RELEVANCE'] = advice_list.GIFT_NAME.map(group_advice)
        advice_list.drop_duplicates(subset=['GIFT_NAME'], inplace=True)
        advice_list.sort_values('RELEVANCE', ascending=False, inplace=True)
        advice_list.rename({
            'GIFT_NAME': 'Назва подарунка',
            'GIFT_PRICE': 'Ціна',
            'GIFT_DESC': 'Опис',
            'RELEVANCE': 'Релевантність'
        }, axis=1, inplace=True)
        return render_template('advice/show_advice_list.html', advice_list=advice_list.to_html())
    return render_template('advice/select_feature.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

