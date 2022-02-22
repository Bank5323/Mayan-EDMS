from django.apps import apps


def handler_user_theme_setting_create(sender, instance, created, **kwargs):
    UserThemeSetting = apps.get_model(
        app_label='appearance', model_name='UserThemeSetting'
    )

    if created:
        UserThemeSetting.objects.create(user=instance)
        

def handler_theme_create(sender, instance, created, **kwargs):
    UserThemeSetting = apps.get_model(
        app_label='appearance', model_name='UserThemeSetting'
    )

    if created:
        stylesheet_text = ".container-fluid{background: "+instance.color_background+";}"+"#menu-main{background-color: "+instance.color_menu+";}"+"#accordion-sidebar{background: "+instance.color_menu+";}"+"#accordion-sidebar .panel-heading{background-color: "+instance.color_menu+";}"
        instance.stylesheet = stylesheet_text
        instance.save()

        ## function to set theme all user (not use)
        
        # print(list(UserThemeSetting.objects.all()))
        # for user in UserThemeSetting.objects.all():
        #     user.theme = instance
        #     user.save()
    
