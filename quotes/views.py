from django.shortcuts import render

def manager(request):
	if request.session.get('user_id', False):
		return render(request, 'manager.html')
	return render(request, 'manager.html')