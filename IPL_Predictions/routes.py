from flask import render_template,redirect,flash,redirect,url_for,session,request
from IPL_Predictions import app
import numpy as np
import pickle

filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))

@app.route('/',methods=['GET','POST'])
def Home():
	if request.method=="POST":
		batting_team = request.form['BatTeam']
		bowling_team = request.form['BowlTeam']
		venue=request.form['Venue']
		ovrs=request.form['overs']
		Runs_Scored=int(request.form['Runs'])
		Wkts=int(request.form['Wickets'])
		Runs_Prev5=int(request.form['RPrev5'])
		Wkts_Prev5=int(request.form['WPrev5'])
		Dec=ovrs.split('.')
		if (len(Dec)==1):
			Dec.append('0')
		if (int(Dec[0])<=19 and int(Dec[1])<=5):
			ovrs=float(ovrs)
			if (batting_team==bowling_team):
				flash('You can not have the same batting and bowling team', 'danger')
				return render_template('Home.html',title='IPL Score-Home')
			elif (ovrs<6):
				flash('Please enter overs value greater than 6', 'danger')
				return render_template('Home.html',title='IPL Score-Home')
			elif (Runs_Prev5>Runs_Scored or Runs_Scored==0):
				flash('Please enter correct input for Runs', 'danger')
				return render_template('Home.html',title='IPL Score-Home')
			elif (Wkts<Wkts_Prev5 or Wkts>=10):
				flash('Please enter correct input for Wickets', 'danger')
				return render_template('Home.html',title='IPL Score-Home')
			else:
				temp_array = []
				print(batting_team)
				print(type(batting_team))
				if batting_team == 'Chennai Super Kings':
					temp_array = temp_array + [1,0,0,0,0,0,0,0]
				elif batting_team == 'Delhi Capitals':
					temp_array = temp_array + [0,1,0,0,0,0,0,0]
				elif batting_team == 'Kings XI Punjab':
					temp_array = temp_array + [0,0,1,0,0,0,0,0]
				elif batting_team == 'Kolkata Knight Riders':
					temp_array = temp_array + [0,0,0,1,0,0,0,0]
				elif batting_team == 'Mumbai Indians':
					temp_array = temp_array + [0,0,0,0,1,0,0,0]
				elif batting_team == 'Rajasthan Royals':
					temp_array = temp_array + [0,0,0,0,0,1,0,0]
				elif batting_team == "Royal Challengers Banglore":
					print(True)
					temp_array = temp_array + [0,0,0,0,0,0,1,0]
				elif batting_team == 'Sunrisers Hyderabad':
					temp_array = temp_array + [0,0,0,0,0,0,0,1]


				if bowling_team == 'Chennai Super Kings':
					temp_array = temp_array + [1,0,0,0,0,0,0,0]
				elif bowling_team == 'Delhi Capitals':
					temp_array = temp_array + [0,1,0,0,0,0,0,0]
				elif bowling_team == 'Kings XI Punjab':
					temp_array = temp_array + [0,0,1,0,0,0,0,0]
				elif bowling_team == 'Kolkata Knight Riders':
					temp_array = temp_array + [0,0,0,1,0,0,0,0]
				elif bowling_team == 'Mumbai Indians':
					temp_array = temp_array + [0,0,0,0,1,0,0,0]
				elif bowling_team == 'Rajasthan Royals':
					temp_array = temp_array + [0,0,0,0,0,1,0,0]
				elif bowling_team == 'Royal Challengers Banglore':
					print(True)
					temp_array = temp_array + [0,0,0,0,0,0,1,0]
				elif bowling_team == 'Sunrisers Hyderabad':
					temp_array = temp_array + [0,0,0,0,0,0,0,1]

				temp_array = temp_array + [ovrs, Runs_Scored, Wkts,Runs_Prev5, Wkts_Prev5]
				temp_array=[temp_array]
				data=np.array(temp_array)
				print(data)
				print(data.shape)
				my_prediction = int(regressor.predict(data))

				if venue == 'Eden Gardens,Kolkata':
					if  ovrs<=14:
						lowers=my_prediction-12
						uppers=my_prediction+8
					else: 
						lowers=my_prediction-8
						uppers=my_prediction+10
				elif venue == 'Arun Jaitely Stadium,Delhi':
					if  ovrs<=14:
						lowers=my_prediction-12
						uppers=my_prediction+8
					else: 
						lowers=my_prediction-8
						uppers=my_prediction+10
				elif venue == 'M Chinnaswamy Stadium,Bengaluru':
					if  ovrs<=14:
						lowers=my_prediction-8
						uppers=my_prediction+12
					else: 
						lowers=my_prediction-5
						uppers=my_prediction+14
				elif venue == 'MA Chidambaram Stadium,Chepauk':
					if  ovrs<=14:
						lowers=my_prediction-8
						uppers=my_prediction+12
					else: 
						lowers=my_prediction-5
						uppers=my_prediction+14
				elif venue == 'PCA Stadium,Mohali':
					if  ovrs<=14:
						lowers=my_prediction-10
						uppers=my_prediction+9
					else: 
						lowers=my_prediction-8
						uppers=my_prediction+10
				elif venue == 'Rajiv Gandhi Internl Stadium,Uppal':
					if  ovrs<=14:
						lowers=my_prediction-13
						uppers=my_prediction+8
					else:
						lowers=my_prediction-8
						uppers=my_prediction+10
				elif venue == 'Sawai Mansingh Stadium,Jaipur':
					if  ovrs<=14:
						lowers=my_prediction-10
						uppers=my_prediction+6
					else: 
						lowers=my_prediction-6
						uppers=my_prediction+12
				elif venue == 'Wankhede Stadium,Mumbai':
					if  ovrs<=14:
						lowers=my_prediction-10
						uppers=my_prediction+14
					else: 
						lowers=my_prediction-5
						uppers=my_prediction+14

				session['var1'] = batting_team
				session['var2'] = bowling_team
				session['var3'] = ovrs
				session['var4'] = Runs_Scored
				session['var5'] = Wkts
				session['var6'] = Runs_Prev5
				session['var7'] = Wkts_Prev5
				session['var8'] = lowers
				session['var9'] = uppers
				session['var10'] = venue
				return redirect(url_for('results'))
		else:
			flash('Please enter correct input for Overs', 'danger')
			return render_template('Home.html',title='IPL Score-Home')
	return render_template('Home.html',title='IPL Score-Home')


@app.route('/results',methods=['GET','POST'])
def results():
	batting_team = session.get('var1')
	bowling_team = session.get('var2')
	ovrs = session.get('var3')
	Runs_Scored = session.get('var4')
	Wkts = session.get('var5')
	Runs_Prev5 = session.get('var6')
	Wkts_Prev5 = session.get('var7')
	lowers = session.get('var8')
	uppers = session.get('var9')
	venue = session.get('var10')
	Bat_CSK = 0
	Bat_DC = 0
	Bat_KXIP = 0
	Bat_KKR = 0
	Bat_MI = 0
	Bat_RR = 0
	Bat_RCB = 0
	Bat_SRH = 0

	Bowl_CSK = 0
	Bowl_DC = 0
	Bowl_KXIP = 0
	Bowl_KKR = 0
	Bowl_MI = 0
	Bowl_RR = 0
	Bowl_RCB = 0
	Bowl_SRH = 0

	if batting_team and bowling_team:
		if batting_team == 'Chennai Super Kings':
			Bat_CSK = 1
		elif batting_team == 'Delhi Capitals':
			Bat_DC = 1
		elif batting_team == 'Kings XI Punjab':
			Bat_KXIP = 1
		elif batting_team == 'Kolkata Knight Riders':
			Bat_KKR = 1
		elif batting_team == 'Mumbai Indians':
			Bat_MI = 1
		elif batting_team == 'Rajasthan Royals':
			Bat_RR = 1
		elif batting_team == 'Royal Challengers Banglore':
			Bat_RCB = 1
		elif batting_team == 'Sunrisers Hyderabad':
			Bat_SRH = 1

		if bowling_team == 'Chennai Super Kings':
			Bowl_CSK = 1
		elif bowling_team == 'Delhi Capitals':
			Bowl_DC = 1
		elif bowling_team == 'Kings XI Punjab':
			Bowl_KXIP = 1
		elif bowling_team == 'Kolkata Knight Riders':
			Bowl_KKR = 1
		elif bowling_team == 'Mumbai Indians':
			Bowl_MI = 1
		elif bowling_team == 'Rajasthan Royals':
			Bowl_RR=1
		elif bowling_team == 'Royal Challengers Banglore':
			Bowl_RCB=1
		elif bowling_team == 'Sunrisers Hyderabad':
			Bowl_SRH=1
		return render_template('Results.html',title='IPL Score-Results',match_venue=venue,ovr=ovrs,Runs=Runs_Scored,Wkts=Wkts,Runs_5=Runs_Prev5,Wkts_5=Wkts_Prev5,Prediction_Lower=lowers,Prediction_Upper=uppers,Bat_CSK = Bat_CSK,Bat_DC = Bat_DC, Bat_KXIP = Bat_KXIP, Bat_KKR = Bat_KKR,Bat_MI = Bat_MI, Bat_RR = Bat_RR, Bat_RCB=Bat_RCB, Bat_SRH = Bat_SRH, Bowl_CSK = Bowl_CSK,Bowl_DC = Bowl_DC,Bowl_KXIP = Bowl_KXIP,Bowl_KKR = Bowl_KKR,Bowl_MI = Bowl_MI ,Bowl_RR = Bowl_RR, Bowl_RCB = Bowl_RCB,Bowl_SRH = Bowl_SRH)
	else:
		return render_template('Home.html',title='IPL Score-Home')