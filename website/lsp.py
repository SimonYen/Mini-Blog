from genericpath import isfile
from flask import Blueprint, render_template, redirect, url_for, request, flash
import os
from . import LSP_FOLDER

lsp=Blueprint("lsp",__name__)

@lsp.route('/lsp/home')
def lsp_home():
	files=os.listdir(LSP_FOLDER)
	nf=[]
	for f in files:
		nf.append('lsp/'+f)
	return render_template('lsp/home.html',files=nf)

@lsp.route('/lsp/upload',methods=['POST','GET'])
def lsp_upload():
	if request.method=='POST':
		file=request.files['file']
		file.save(os.path.join(LSP_FOLDER,file.filename))
		return redirect(url_for('lsp.lsp_home'))
	return render_template('lsp/upload.html')

@lsp.route('/lsp/manage/',methods=['POST','GET'])
def lsp_manage():
	files=os.listdir(LSP_FOLDER)
	if request.method=='POST':
		new_name=request.form.get('new_name')
		old_name=request.form.get('old_name')
		if os.path.isfile(os.path.join(LSP_FOLDER,old_name)):
			os.rename(os.path.join(LSP_FOLDER,old_name),os.path.join(LSP_FOLDER,new_name))
			return redirect(url_for('lsp.lsp_home'))
	return render_template('lsp/manage.html',files=files)

@lsp.route('/lsp/delete/<name>')
def lsp_delete(name):
	if os.path.isfile(os.path.join(LSP_FOLDER,name)):
		os.remove(os.path.join(LSP_FOLDER,name))
	return redirect(url_for('lsp.lsp_home'))