from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import db, User, ShoppingList, Item
from .forms import RegisterForm, LoginForm, ListForm, ItemForm

bp = Blueprint("routes", __name__)

# ---------- Auth ----------
@bp.get("/register")
def register():
    form = RegisterForm()
    return render_template("register.html", form=form)

@bp.post("/register")
def register_post():
    form = RegisterForm()
    if not form.validate_on_submit():
        flash("Please correct the errors in the form.", "danger")
        return render_template("register.html", form=form), 400
    email = form.email.data.strip().lower()
    if User.query.filter_by(email=email).first():
        flash("Email already registered.", "danger")
        return render_template("register.html", form=form), 400
    user = User(email=email)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash("Account created. Please log in.", "success")
    return redirect(url_for("routes.login"))

@bp.get("/login")
def login():
    form = LoginForm()
    return render_template("login.html", form=form)

@bp.post("/login")
def login_post():
    form = LoginForm()
    if not form.validate_on_submit():
        flash("Please fill in your credentials.", "danger")
        return render_template("login.html", form=form), 400
    email = form.email.data.strip().lower()
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(form.password.data):
        flash("Invalid credentials.", "danger")
        return render_template("login.html", form=form), 401
    login_user(user)
    return redirect(url_for("routes.dashboard"))

@bp.post("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("routes.login"))

# ---------- Dashboard ----------
@bp.get("/")
@login_required
def dashboard():
    q = request.args.get("q", "").strip()
    lists = ShoppingList.query.filter_by(user_id=current_user.id)
    if q:
        lists = lists.filter(ShoppingList.name.ilike(f"%{q}%"))
    lists = lists.order_by(ShoppingList.created_at.desc()).all()
    list_form = ListForm()
    return render_template("dashboard.html", lists=lists, q=q, list_form=list_form)

@bp.post("/lists/new")
@login_required
def create_list():
    form = ListForm()
    if not form.validate_on_submit():
        flash("List name is required.", "danger")
        return redirect(url_for("routes.dashboard"))
    sl = ShoppingList(name=form.name.data.strip(), user_id=current_user.id)
    db.session.add(sl)
    db.session.commit()
    flash("List created.", "success")
    return redirect(url_for("routes.view_list", list_id=sl.id))

@bp.post("/lists/<int:list_id>/delete")
@login_required
def delete_list(list_id):
    sl = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    db.session.delete(sl)
    db.session.commit()
    flash("List deleted.", "success")
    return redirect(url_for("routes.dashboard"))

# ---------- List detail & items ----------
@bp.get("/lists/<int:list_id>")
@login_required
def view_list(list_id):
    sl = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    items = Item.query.filter_by(list_id=sl.id).order_by(Item.created_at.desc()).all()
    item_form = ItemForm()
    list_form = ListForm(name=sl.name)
    return render_template("list_detail.html", sl=sl, items=items, item_form=item_form, list_form=list_form)

@bp.post("/lists/<int:list_id>/edit")
@login_required
def edit_list(list_id):
    sl = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    form = ListForm()
    if not form.validate_on_submit():
        flash("Name required.", "danger")
        return redirect(url_for("routes.view_list", list_id=list_id))
    sl.name = form.name.data.strip()
    db.session.commit()
    flash("List renamed.", "success")
    return redirect(url_for("routes.view_list", list_id=list_id))

@bp.post("/lists/<int:list_id>/items")
@login_required
def add_item(list_id):
    sl = ShoppingList.query.filter_by(id=list_id, user_id=current_user.id).first_or_404()
    form = ItemForm()
    if not form.validate_on_submit():
        flash("Please provide item details.", "danger")
        return redirect(url_for("routes.view_list", list_id=list_id))
    it = Item(name=form.name.data.strip(),
              quantity=form.quantity.data or 1,
              priority=form.priority.data,
              list=sl)
    db.session.add(it)
    db.session.commit()
    flash("Item added.", "success")
    return redirect(url_for("routes.view_list", list_id=list_id))

@bp.post("/items/<int:item_id>/toggle")
@login_required
def toggle_item(item_id):
    it = Item.query.get_or_404(item_id)
    if it.list.owner.id != current_user.id:
        return ("Forbidden", 403)
    it.purchased = not it.purchased
    db.session.commit()
    flash("Item updated.", "success")
    return redirect(url_for("routes.view_list", list_id=it.list_id))

@bp.post("/items/<int:item_id>/delete")
@login_required
def delete_item(item_id):
    it = Item.query.get_or_404(item_id)
    if it.list.owner.id != current_user.id:
        return ("Forbidden", 403)
    list_id = it.list_id
    db.session.delete(it)
    db.session.commit()
    flash("Item deleted.", "success")
    return redirect(url_for("routes.view_list", list_id=list_id))
