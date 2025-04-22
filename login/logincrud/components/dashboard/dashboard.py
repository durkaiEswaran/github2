from django_components import component

@component.register("sidebar")
class Table(component.Component):
        template_name="dashboard/dashboard_menu.html"  
        
        def get_context_data(self):
                return{
                    
                    }
        class Media:
            css='dashboard/style.css',
            # js='sidebar/script.js'