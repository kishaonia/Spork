from flask import Blueprint, jsonify, session, request
from app.models import User, db, Post
from .auth_routes import validation_errors_to_error_messages
from app.forms import PostForm
from flask_login import current_user, login_required

post_routes = Blueprint('posts', __name__)



@post_routes.route('/')
def posts():
    """
    Query for all posts and returns them in a list of post dictionaries
    """
    posts = Post.query.all()
    return_list = []
    for post in posts:
        post_dict = post.to_dict()
        owner = post.owner
        post_dict['owner'] = owner.to_dict()
        return_list.append(post_dict)
    return return_list

@post_routes.route('/current_user')
@login_required
def current_user_posts():
    """
    Query for all user's posts and returns them in a list of post dictionaries
    """

    current_user_dict = current_user.to_dict()
    posts = Post.query.filter(Post.userId == current_user_dict['id'])
    return_list = []
    for post in posts:
        post_dict = post.to_dict()
        owner = post.owner
        post_dict['owner'] = owner.to_dict()
        return_list.append(post_dict)
    return return_list


@post_routes.route('/create', methods=['POST'])
@login_required
def create_a_post():
    form = PostForm()
    current_user_dict = current_user.to_dict()
    form['csrf_token'].data = request.cookies['csrf_token']
    if form.validate_on_submit():
        new_post = Post(
            content=form.data['content'],
            userId=current_user_dict['id']
        )
        db.session.add(new_post)
        db.session.commit()
        return {"Successfully Created Post": new_post.to_dict()}
    return {'errors': validation_errors_to_error_messages(form.errors)}, 401



@post_routes.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete_post(id):
    to_delete = Post.query.get(id)
    db.session.delete(to_delete)
    db.session.commit()
    return {"Message": "Post Delete Successfully"}