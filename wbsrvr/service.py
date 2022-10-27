import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import controller

bp = Blueprint('service', __name__, url_prefix='/service')

cont = controller.control()
mode = None

#Getting info of user requirement
@bp.route('/req', methods = ('GET', 'POST'))
def req():
	global mode
	if request.method == 'POST':
		noofpads = request.form['Qty']
		mode = request.form['Mode']
		error = None
		
		if not noofpads:
			error = 'No of pads are required'

		if error is None:
			return redirect(url_for("service.process"))
		flash(error)
	return render_template('service/req.html')

@bp.route('/paycoin')
def paycoin():
	if cont.status == 's':
		return redirect(url_for("service.done"))
	elif cont.status == 'q':
		return redirect(url_for("service.cfail"))
	return render_template('payment/paycoin.html')

@bp.route('/process')
def process():
	global mode
	cont.status = None
	cont.paychk(mode)
	return redirect(url_for("service.paycoin"))

@bp.route('/done')
def done():
	cont.status = None
	return render_template('payment/done.html')

@bp.route('/cfail')
def cfail():
	cont.status = None
	return render_template('payment/cfail.html')
