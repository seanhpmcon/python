from django.shortcuts import redirect
from ldap3 import Server, Connection

class LDAPAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        
        if request.path == '/attendance/login' and request.method == 'POST':
            un = request.POST.get('username')
            pw = request.POST.get('password')
            
            server = Server('ldap://ttbrcdc001.ad.pmcon.co.tt')

            conn = Connection(server, user=f'PMCON\\{un}', password=pw)

            if not conn.bind():
                return redirect('/attendance/login?login=fail1')
            
            request.session['ldap_name'] = un
            
        if 'ldap_name' not in request.session and request.path != '/attendance/login':
            return redirect('/attendance/login')
        
        if request.path == '/attendance/login' and 'ldap_name' in request.session:
            return redirect('/attendance/')
        
        response = self.get_response(request)

        return response