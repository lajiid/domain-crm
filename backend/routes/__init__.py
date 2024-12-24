from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os

main = Blueprint("main", __name__)

def register_routes(app):
    # 注册蓝图
    app.register_blueprint(main)

@main.route("/api/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "没有文件"}), 400
    
    file = request.files["file"]
    
    if file.filename == "":
        return jsonify({"error": "未选择文件"}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)
        
        return jsonify({
            "message": "文件上传成功",
            "filename": filename,
            "path": file_path
        }), 200
    
    return jsonify({"error": "文件类型不允许"}), 400

def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]
