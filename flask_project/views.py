from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from . import User, UserOrder, Product, app, bcrypt, db, forms


@app.route('/')
def index():
    return render_template('homepage.html')


@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    form = forms.SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode('utf-8')
        user = User(username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Registration succeeded, {user.username}, now you can sign in.', 'success')
        return redirect(url_for('index'))
    return render_template('sign_up.html', form=form)


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = forms.SignInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            flash(f'User {form.username.data} does not exist!', 'danger')
            return redirect(url_for('sign_in'))
        if not bcrypt.check_password_hash(user.password, form.password.data):
            flash(f'User / password do not match!', 'danger')
            return redirect(url_for('sign_in'))
        login_user(user)
        flash(f'Welcome, {user.username}', 'success')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('sign_in.html', form=form)


@app.route('/sign_out')
def sign_out():
    flash(f'See you next time, {current_user.username}')
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    form = forms.CreateProductForm()
    if form.validate_on_submit():
        product = Product(name=form.name.data, code=form.code.data)
        db.session.add(product)
        db.session.commit()
        flash(f'Product {product.name} created.', 'success')
        return redirect(url_for('add_product'))
    return render_template('add_product.html', form=form)


@app.route('/show_product_item/<product_id>')
def show_product_item(product_id):
    product = Product.query.get(product_id)
    return render_template('show_product_item.html', product=product)


@app.route('/show_products')
def show_products():
    products = Product.query.all()
    return render_template('show_products.html', products=products)


@app.route('/add_user_order', methods=['GET', 'POST'])
@login_required
def add_user_order():
    form = forms.CreateUserOrderForm()
    if form.validate_on_submit():
        order = UserOrder(
            product_id=form.product.data.id
            , quantity=form.quantity.data
            , user_id=current_user.id
        )
        db.session.add(order)
        db.session.commit()
        flash('Order created', 'success')
        return redirect(url_for('add_user_order'))
    return render_template('add_user_order.html', form=form)


@app.route('/show_user_orders')
@login_required
def show_user_orders():
    orders = UserOrder.query.filter_by(user_id=current_user.id).all()
    return render_template('show_user_orders.html', data=orders)


@app.route('/user_account', methods=['GET', 'POST'])
@login_required
def user_account():
    form = forms.UpdateUserAccount()
    if request.method == 'GET':
        form.username.data = current_user.username
    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.username = form.username.data
        db.session.add(user)
        db.session.commit()
        flash('Your account was updated successfully', 'success')
        redirect(url_for('user_account'))
    return render_template('user_account.html', form=form)
