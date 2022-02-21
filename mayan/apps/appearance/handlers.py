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
        instance.stylesheet = "body{background-color: "+instance.color+";}"
        instance.save()

        ## function to set theme all user
        
        # print(list(UserThemeSetting.objects.all()))
        # for user in UserThemeSetting.objects.all():
        #     user.theme = instance
        #     user.save()
    
