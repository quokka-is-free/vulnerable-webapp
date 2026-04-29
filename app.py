"""
Helix Systems Internal Portal - Vulnerable Web App
ASM 시연용 의도적 취약 웹 애플리케이션
실제 운영 환경 절대 배포 금지
"""
from flask import Flask, request, render_template, redirect, send_file, jsonify, make_response
import os
import io

app = Flask(__name__)
app.secret_key = "helix_demo_secret_key_2026"


# ============================================
# 1. 메인 페이지 (정상)
# ============================================
@app.route("/")
def index():
    return render_template("index.html")


# ============================================
# 2. 로그인 페이지 - SQL Injection 의도
# ============================================
@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # 의도적 취약 - SQL Injection 패턴 감지 시 DB 에러 메시지 노출
        if "'" in username or "--" in username or '"' in username:
            error = (
                f"DB Error: SQL syntax error near '{username}' "
                f"at line 1 of SELECT * FROM users WHERE username='{username}' "
                f"AND password='{password}' [MySQL 5.7.32]"
            )
        elif username == "admin" and password == "admin123":
            return redirect("/admin")
        else:
            error = "Invalid username or password."

    return render_template("login.html", error=error)


# ============================================
# 3. 관리자 페이지 - Broken Access Control (인증 우회)
# ============================================
@app.route("/admin")
def admin():
    # 의도적 취약 - 세션 검증 로직 누락
    return render_template("admin.html")


# ============================================
# 4. 검색 페이지 - Reflected XSS
# ============================================
@app.route("/search")
def search():
    query = request.args.get("q", "")
    return render_template("search.html", query=query)


# ============================================
# 5. API 엔드포인트 - Information Disclosure (인증 없음)
# ============================================
@app.route("/api/v1/users")
def api_users():
    # 의도적 취약 - 인증 없이 사내 임직원 정보 평문 노출
    return jsonify({
        "status": "ok",
        "count": 5,
        "users": [
            {"id": 1, "username": "admin", "email": "admin@helix-systems.com",
             "role": "Administrator", "department": "IT", "phone": "010-1234-5678"},
            {"id": 2, "username": "j.kim", "email": "junseo.kim@helix-systems.com",
             "role": "Developer", "department": "Engineering", "phone": "010-2345-6789"},
            {"id": 3, "username": "s.park", "email": "soyeon.park@helix-systems.com",
             "role": "Designer", "department": "Product", "phone": "010-3456-7890"},
            {"id": 4, "username": "h.lee", "email": "hyunwoo.lee@helix-systems.com",
             "role": "Security Engineer", "department": "Security", "phone": "010-4567-8901"},
            {"id": 5, "username": "m.choi", "email": "minji.choi@helix-systems.com",
             "role": "PM", "department": "Product", "phone": "010-5678-9012"},
        ]
    })


# ============================================
# 6. .env 노출 - Sensitive File Exposure
# ============================================
@app.route("/.env")
def env_file():
    content = """# Helix Systems Production Environment
# DO NOT COMMIT THIS FILE

DB_HOST=db.helix-systems.internal
DB_PORT=3306
DB_USER=helix_admin
DB_PASSWORD=H3l!x_Pr0d_2026_$ecret

API_KEY=sk_live_4eC39HqLyjWDarjtT1zdp7dc
JWT_SECRET=helix_jwt_secret_key_do_not_share
AWS_ACCESS_KEY_ID=AKIA1234567890ABCDEF
AWS_SECRET_ACCESS_KEY=abcdefghij1234567890KLMNOPQRSTUVWXYZ12345

REDIS_URL=redis://redis.helix-systems.internal:6379
SMTP_PASSWORD=smtp_helix_2026

DEBUG=False
ENVIRONMENT=production
"""
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


# ============================================
# 7. .git/config 노출 - Sensitive File Exposure
# ============================================
@app.route("/.git/config")
def git_config():
    content = """[core]
\trepositoryformatversion = 0
\tfilemode = true
\tbare = false
\tlogallrefupdates = true
[remote "origin"]
\turl = git@github.com:helix-systems/internal-portal.git
\tfetch = +refs/heads/*:refs/remotes/origin/*
[branch "main"]
\tremote = origin
\tmerge = refs/heads/main
[branch "develop"]
\tremote = origin
\tmerge = refs/heads/develop
[user]
\tname = Hyunwoo Lee
\temail = hyunwoo.lee@helix-systems.com
"""
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


# ============================================
# 8. phpinfo - Misconfiguration
# ============================================
@app.route("/phpinfo.php")
def phpinfo():
    return render_template("phpinfo.html")


# ============================================
# 9. 백업 파일 노출 - Misconfiguration
# ============================================
@app.route("/backup.zip")
def backup_zip():
    # 가짜 ZIP 헤더 + 더미 데이터
    fake_zip = (
        b"PK\x03\x04\x14\x00\x00\x00\x08\x00"
        b"# Helix Systems Backup - 2026-01-15\n"
        b"# This is a demo file for ASM scanner testing\n"
        b"# In real-world: source code, database dumps, configs\n"
        b"PK\x05\x06\x00\x00\x00\x00"
    )
    return send_file(
        io.BytesIO(fake_zip),
        mimetype="application/zip",
        as_attachment=True,
        download_name="backup.zip"
    )


# ============================================
# 10. robots.txt - 추가 정보 노출
# ============================================
@app.route("/robots.txt")
def robots():
    content = """User-agent: *
Disallow: /admin
Disallow: /backup
Disallow: /api/v1
Disallow: /.env
Disallow: /.git
Disallow: /phpinfo.php
Disallow: /internal/

# Helix Systems - Internal Portal
"""
    response = make_response(content)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


# ============================================
# 헬스 체크
# ============================================
@app.route("/healthz")
def healthz():
    return {"status": "ok", "service": "helix-internal-portal"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
