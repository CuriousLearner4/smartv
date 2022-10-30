import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from . import RPimanager

bp = Blueprint('service', __name__, url_prefix='/service')

manager = RPimanager.RPiManager()

msg = 'hero'
#Getting info of user requirement
@bp.route('/req', methods = ('GET', 'POST'))
def req():
	if request.method == 'POST':
		manager.quantity = request.form['Qty']
		manager.mode = request.form['Mode']
		error = None

		if not manager.quantity:
			error = 'No of pads are required'

		if error is None:
			return redirect(url_for("service.process"))
		flash(error)
	return render_template('service/req.html')

@bp.route('/payrfid', methods = ('GET', 'POST'))
def payrfid():
	if request.method == 'POST':
		if manager.dispenseflag == True:
			manager.pad_dispenser()
			return redirect(url_for("service.dispensing"))
		elif manager.dispenseflag == False:
			return redirect(url_for("service.req"))

	return render_template('payment/rfid.html',name = manager.message, state = manager.dispenseflag)
	
@bp.route('/coin')
def coin():
	if manager.dispenseflag == True:
		manager.pad_dispenser()
		return redirect(url_for("service.dispensing"))
	elif manager.dispenseflag == False:
		return redirect(url_for("service.cfail"))
	 
@bp.route('/dispensing')
def dispensing():
	if manager.dispensestatus == 'done':
		return redirect(url_for("service.done"))
	elif manager.dispensestatus == 'failed' or manager.dispenseflag == False:
		return redirect(url_for("service.cfail"))
	return render_template('service/dispensing.html',name1 = manager.message1)

@bp.route('/process')
def process():
	manager.payment_processor()
	if manager.mode == 'rfid':
		return redirect(url_for("service.payrfid"))
	elif manager.mode == 'coin':
		return redirect(url_for("service.coin"))
	elif manager.mode == 'qr':
		return redirect(url_for("service.qr"))

@bp.route('/done')
def done():
	manager.clean_up()
	return render_template('payment/done.html')

@bp.route('/cfail')
def cfail():
	manager.clean_up()
	return render_template('payment/cfail.html')