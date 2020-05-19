from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post,City,Country,Image,User
from flaskblog.posts.forms import PostForm
from flaskblog.posts.utils import save_picture

posts = Blueprint('posts', __name__)

@posts.route("/posts")
def browse():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    cities = City.query.all()
    countries = Country.query.all()
    if not posts:
        posts=[]
    return render_template('browse.html', posts=posts,cities=cities,countries=countries)

@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    cities=[(c.name, c.name) for c in City.query.all()]
    countries=[(c.name, c.name) for c in Country.query.all()]
    form = PostForm(city_choices=cities,country_choices=countries)
    
    if form.validate_on_submit():
        city = City.query.filter_by(name=form.city.data).first()
        post = Post(title=form.title.data, content=form.content.data, author=current_user,
        anouncement_type=form.postType.data,house_type=form.houseType.data,square_meters=form.sqMeters.data,
        price=form.price.data,address=form.address.data,city_id=city.id,number_rooms=form.nmbRooms.data,phonenumber=form.phonenumber.data)
        
        if form.picture.data:
            for pic in form.picture.data:
                pic_name = save_picture(pic)
                image = Image(name=pic_name,post=post)
                db.session.add(image)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('posts.post',post_id=post.id))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    images = Image.query.filter_by(post_id=post_id)
    return render_template('post.html',images=images, title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    update=True
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    cities=[(c.name, c.name) for c in City.query.all()]
    countries=[(c.name, c.name) for c in Country.query.all()]
    form = PostForm(city_choices=cities,country_choices=countries)
    if form.validate_on_submit():
        post.title = form.title.data
        post.price = form.price.data
        post.square_meters = form.sqMeters.data
        post.number_rooms = form.nmbRooms.data
        post.phonenumber = form.phonenumber.data
        post.address = form.address.data
        post.content = form.content.data
        post.anouncement_type = form.postType.data
        post.house_type = form.houseType.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
        form.price.data = post.price
        form.sqMeters.data = post.square_meters
        form.nmbRooms.data = post.number_rooms
        form.address.data = post.address
        form.phonenumber.data = post.phonenumber
        form.postType.data = dict(form.postType.choices).get(post.anouncement_type)
        form.houseType.data = dict(form.houseType.choices).get(post.house_type)

    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post',update=update,images=post.images)


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('posts.browse'))

@posts.route("/favorite/user/<int:user_id>/post/<int:post_id>/", methods=['POST'])
@login_required
def favorite_post(user_id,post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)
    if post.author == user:
        abort(403)
    user.favorites.append(post)
    flash('The post has been added to favorites!', 'success')
    return redirect(url_for('posts.post',post_id=post_id))