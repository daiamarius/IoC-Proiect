from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post,City,Country,Image
from flaskblog.posts.forms import PostForm
from flaskblog.posts.utils import save_picture

posts = Blueprint('posts', __name__)


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
        price=form.price.data,address=form.address.data,city_id=city.id,number_rooms=form.nmbRooms.data)
        
        if form.picture.data:
            for pic in form.picture.data:
                pic_name = save_picture(pic)
                image = Image(name=pic_name,post=post)
                db.session.add(image)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    images = Image.query.filter_by(post_id=post_id)
    return render_template('test.html',images=images, title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

