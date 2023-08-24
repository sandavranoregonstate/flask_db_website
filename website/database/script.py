from flask import flash

def flashMessage(attribute='', charCount=0, crud='', message=''):
    if crud == 'create':
        flash(f"Entry added!", category='success')
    elif crud == 'update':
        flash(f"Entry updated!", category='success')
    elif crud == 'custom':
        flash(message, category='error')
    else: 
        flash(f"{attribute} must be greater than {charCount} character(s)", category='error')
