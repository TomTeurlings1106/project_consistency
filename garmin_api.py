#!/usr/bin/env python3
"""
Garmin Connect API integration for habit tracker
"""

import os
import json
from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_cors import CORS
from garminconnect import Garmin
from supabase import create_client, Client

app = Flask(__name__)
CORS(app)

# Supabase configuration
SUPABASE_URL = "https://bsyyvvaytupjuxwecwrq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJzeXl2dmF5dHVwanV4d2Vjd3JxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTEzOTI3OTcsImV4cCI6MjA2Njk2ODc5N30.2GjiRkul9y3XT_IFDYhYsUz0cb7TDBqbAugO5cZHxm4"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Garmin client (will be initialized after login)
garmin_client = None

@app.route('/garmin/login', methods=['POST'])
def garmin_login():
    """Login to Garmin Connect"""
    global garmin_client
    
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400
    
    try:
        garmin_client = Garmin(email, password)
        garmin_client.login()
        return jsonify({"success": True, "message": "Successfully connected to Garmin Connect"})
    except Exception as e:
        return jsonify({"error": f"Failed to connect to Garmin: {str(e)}"}), 401

@app.route('/garmin/sync', methods=['POST'])
def sync_garmin_data():
    """Sync Garmin data to database"""
    if not garmin_client:
        return jsonify({"error": "Not logged in to Garmin Connect"}), 401
    
    try:
        # Get date range (last 7 days by default)
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
        
        results = {}
        
        # Sync sleep data
        sleep_data = sync_sleep_data(start_date, end_date)
        results['sleep'] = sleep_data
        
        # Sync steps data
        steps_data = sync_steps_data(start_date, end_date)
        results['steps'] = steps_data
        
        # Sync heart rate data
        hr_data = sync_heart_rate_data(start_date, end_date)
        results['heart_rate'] = hr_data
        
        # Sync activities
        activities_data = sync_activities_data(start_date, end_date)
        results['activities'] = activities_data
        
        return jsonify({
            "success": True,
            "message": f"Synced data from {start_date} to {end_date}",
            "results": results
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to sync data: {str(e)}"}), 500

def sync_sleep_data(start_date, end_date):
    """Sync sleep data to Supabase"""
    synced_count = 0
    current_date = start_date
    
    while current_date <= end_date:
        try:
            sleep_data = garmin_client.get_sleep_data(current_date.isoformat())
            
            if sleep_data and 'dailySleepDTO' in sleep_data:
                sleep_info = sleep_data['dailySleepDTO']
                
                # Prepare data for Supabase
                sleep_record = {
                    'date': current_date.isoformat(),
                    'duration_minutes': sleep_info.get('sleepTimeSeconds', 0) // 60,
                    'deep_sleep_minutes': sleep_info.get('deepSleepSeconds', 0) // 60,
                    'light_sleep_minutes': sleep_info.get('lightSleepSeconds', 0) // 60,
                    'rem_sleep_minutes': sleep_info.get('remSleepSeconds', 0) // 60,
                    'awake_minutes': sleep_info.get('awakeSleepSeconds', 0) // 60,
                    'sleep_score': sleep_info.get('overallSleepScore')
                }
                
                # Insert/update in Supabase
                result = supabase.table('garmin_sleep').upsert(sleep_record).execute()
                synced_count += 1
                
        except Exception as e:
            print(f"Error syncing sleep data for {current_date}: {e}")
        
        current_date += timedelta(days=1)
    
    return {"synced_days": synced_count}

def sync_steps_data(start_date, end_date):
    """Sync steps data to Supabase"""
    synced_count = 0
    current_date = start_date
    
    while current_date <= end_date:
        try:
            steps_data = garmin_client.get_steps_data(current_date.isoformat())
            
            if steps_data:
                steps_record = {
                    'date': current_date.isoformat(),
                    'steps': steps_data.get('totalSteps', 0),
                    'goal': steps_data.get('dailyStepGoal', 10000),
                    'distance_meters': steps_data.get('totalDistance', 0),
                    'floors_climbed': steps_data.get('floorsAscended', 0)
                }
                
                result = supabase.table('garmin_steps').upsert(steps_record).execute()
                synced_count += 1
                
        except Exception as e:
            print(f"Error syncing steps data for {current_date}: {e}")
        
        current_date += timedelta(days=1)
    
    return {"synced_days": synced_count}

def sync_heart_rate_data(start_date, end_date):
    """Sync heart rate data to Supabase"""
    synced_count = 0
    current_date = start_date
    
    while current_date <= end_date:
        try:
            hr_data = garmin_client.get_heart_rates(current_date.isoformat())
            
            if hr_data and 'heartRateValues' in hr_data:
                hr_values = hr_data['heartRateValues']
                if hr_values:
                    # Calculate average HR for the day
                    valid_hrs = [hr for hr in hr_values if hr and hr > 0]
                    
                    if valid_hrs:
                        hr_record = {
                            'date': current_date.isoformat(),
                            'resting_hr': hr_data.get('restingHeartRate'),
                            'max_hr': max(valid_hrs),
                            'avg_hr': sum(valid_hrs) // len(valid_hrs)
                        }
                        
                        result = supabase.table('garmin_heart_rate').upsert(hr_record).execute()
                        synced_count += 1
                
        except Exception as e:
            print(f"Error syncing heart rate data for {current_date}: {e}")
        
        current_date += timedelta(days=1)
    
    return {"synced_days": synced_count}

def sync_activities_data(start_date, end_date):
    """Sync activities data to Supabase"""
    synced_count = 0
    
    try:
        # Get activities for date range
        activities = garmin_client.get_activities_by_date(
            start_date.isoformat(), 
            end_date.isoformat()
        )
        
        for activity in activities:
            activity_record = {
                'date': datetime.fromisoformat(activity['startTimeLocal'].replace('Z', '+00:00')).date().isoformat(),
                'activity_type': activity.get('activityType', {}).get('typeKey', 'unknown'),
                'duration_minutes': activity.get('duration', 0) // 60,
                'calories': activity.get('calories'),
                'distance_meters': activity.get('distance'),
                'heart_rate_avg': activity.get('averageHR'),
                'heart_rate_max': activity.get('maxHR'),
                'activity_start': activity.get('startTimeLocal')
            }
            
            result = supabase.table('garmin_activities').insert(activity_record).execute()
            synced_count += 1
            
    except Exception as e:
        print(f"Error syncing activities data: {e}")
    
    return {"synced_activities": synced_count}

@app.route('/garmin/status', methods=['GET'])
def garmin_status():
    """Check Garmin connection status"""
    return jsonify({
        "connected": garmin_client is not None,
        "message": "Connected to Garmin Connect" if garmin_client else "Not connected to Garmin Connect"
    })

@app.route('/garmin/latest-data', methods=['GET'])
def get_latest_garmin_data():
    """Get latest Garmin data from database"""
    try:
        today = datetime.now().date().isoformat()
        
        # Get latest sleep data
        sleep_result = supabase.table('garmin_sleep').select('*').eq('date', today).execute()
        sleep_data = sleep_result.data[0] if sleep_result.data else None
        
        # Get latest steps data
        steps_result = supabase.table('garmin_steps').select('*').eq('date', today).execute()
        steps_data = steps_result.data[0] if steps_result.data else None
        
        # Get latest heart rate data
        hr_result = supabase.table('garmin_heart_rate').select('*').eq('date', today).execute()
        hr_data = hr_result.data[0] if hr_result.data else None
        
        # Get recent activities (last 7 days)
        week_ago = (datetime.now().date() - timedelta(days=7)).isoformat()
        activities_result = supabase.table('garmin_activities').select('*').gte('date', week_ago).order('date', desc=True).execute()
        activities_data = activities_result.data
        
        return jsonify({
            "sleep": sleep_data,
            "steps": steps_data,
            "heart_rate": hr_data,
            "recent_activities": activities_data
        })
        
    except Exception as e:
        return jsonify({"error": f"Failed to get latest data: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)