from modules import (
    app,
    login_manager
)
from flask import (
    render_template, 
    request, 
    redirect, 
    url_for,
    flash,
    jsonify
)
from flask_login import (
    login_user, 
    login_required, 
    current_user, 
    logout_user
)
from Users import User
import access_db



user_profile = {}


@login_manager.user_loader
def load_user(user_id):
    '''
    回傳給 LoginManager 底下的 user_loader
    登入時要做驗證使用者 der~
    '''
    # 回傳使用者資訊
    query_seq = access_db.query(tablename="Users", target={"user_id": user_id})
    if len(query_seq) == 0:
        return None
    
    id = query_seq[0][0]
    username = query_seq[0][1]
    email = query_seq[0][2]
    password = query_seq[0][3]
    user = User(
        id=id,
        username=username,
        email=email
    )
    user.hashed_password = password
    return user


@app.route("/")
def home():
    return render_template("home.html", user=current_user)


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return redirect(url_for("home"))

    query_seq = access_db.query(tablename="Users", target={"email": email})
    if not query_seq:
        return jsonify(success=False, message='登入失敗：帳號或密碼錯誤')

    user = User(
        id=query_seq[0][0],
        username=query_seq[0][1],
        email=query_seq[0][2]
    )
    user.hashed_password = query_seq[0][3]
    if not user.verify_password(password):
        return jsonify(success=False, message='登入失敗：密碼錯誤')

    login_user(user)
    return jsonify(success=True, message='登入成功！歡迎回來～', redirect_url=url_for("home"))


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return redirect(url_for("home"))

    query_seq = access_db.query(tablename="Users", target={"email": email})
    if query_seq:
        flash("已經註冊過了！請移駕至登入介面。")
        return jsonify(success=False, message="此電子郵件已被註冊過了！請移駕至登入介面。")

    user = User(
        username=username,
        email=email,
        password=password
    )
    access_db.insert_data(tablename="Users", 
                          data={
                              "username": user.username,
                              "email": user.email,
                              "password": user.hashed_password
                          })
    return jsonify(success=True, message=f'註冊成功！歡迎 {username}')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
