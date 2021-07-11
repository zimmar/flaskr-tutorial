import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flaskr.db import get_db

bp = Blueprint('server', __name__, url_prefix='/server')

@bp.route('/add', methods=('GET', 'POST'))
def add():
    
    if request.method == 'POST':
        host_name = request.form['host_name']
        instance_name = request.form['instance_name']
        description = request.form['description']
        
        ip = request.form['ip']
        port = request.form['port']
        
        default = request.form['default']
        library_client = request.form['library_client']
        active = request.form['active']
        
        
        db = get_db()
        error = None
        
        if not host_name:
            error = 'Hostname is required.'
        elif not instance_name:
            error = 'Instancename is required.'
            
        elif db.execute(
            "SELECT id FROM CFG_SERVERS WHERE host_name=? and instance_name=?", (host_name, instance_name)
        ).fetchone() is not None:
            error = f"Server {host_name} with instance {instance_name} is already registered."
        if error is None:
            db.execute (
                "INSERT INTO cfg_servers (host_name, instance_name, description, ip, port, default, library_client, active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (host_name, instance_name, description, ip, port, default, library_client, active)"
            )
            db.commit()
            return redirect(url_for('server.list'))
            
        flash(error)
    
    return render_template('pytsm/server/add.html')

@bp.route('/list', methods=('GET',))
def list():
    db = get_db()
    servers = db.execute("SELECT * FROM cfg_servers").fetchall()
    
    return render_template('pytsm/server/list.html', servers=servers)
    
    
        
            
        
            
        
        
            