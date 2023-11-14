from django.shortcuts import redirect
from ldap3 import Server, Connection

class LDAPAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        
        if request.path == '/auth/login' and request.method == 'POST':
            un = request.POST.get('username')
            pw = request.POST.get('password')
            print('test1')
            
            server = Server('ldap://ttbrcdc001.ad.pmcon.co.tt')

            conn = Connection(server, user=f'PMCON\\{un}', password=pw)

            if not conn.bind():
                return redirect('/auth/login?login=fail1')
            
            request.session['ldap_name'] = un
            
        if 'ldap_name' not in request.session and request.path != '/auth/login':
            print(request.path)
            print(request.session['ldap_name'])
            return redirect('/auth/login')
        
        if request.path == '/auth/login' and 'ldap_name' in request.session:
            print('test3')
            return redirect('/attendance/')
        
        response = self.get_response(request)

        return response