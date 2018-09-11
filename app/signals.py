from django.db.models.signals import * 
from django.dispatch import receiver
from app.models import * 
from django.template import loader, Context
from django.template.loader import get_template
from payout import *


#exclude some fields from diff
exclude_fields = ['FanDuelSalary','FantasyPointsFanDuel']

def model_to_dict(m):
    d = dict([(field.attname, getattr(m, field.attname))
        for field in m._meta.local_fields if not isinstance(field, models.ForeignKey )])

    for ex in exclude_fields:
        d.pop(ex, None)
        
    return d




@receiver(pre_save, sender=PlayerGame)
def diff_player_changes(sender, instance, **kwargs):
    diff_changes(sender, instance, **kwargs)

@receiver(pre_save, sender=TeamGame)
def diff_team_changes(sender, instance, **kwargs):
    diff_changes(sender, instance, **kwargs)



@receiver(pre_save, sender=Timeframe)
def diff_timeframe_changes(sender, instance, **kwargs):
    # different rules, since we are not working with polymorphic type

    print "saving timeframe"
    try:
        was = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # For now, not sending initial object write changes.  Must consider as we test...
        None
    else:
        if (was.HasGames    != instance.HasGames):
            None
        if (was.HasStarted  != instance.HasStarted):
            None   
        if (was.HasEnded    != instance.HasEnded):
            None      
        if (was.HasFirstGameStarted!= instance.HasFirstGameStarted):
            None  
        if (was.HasFirstGameEnded  != instance.HasFirstGameEnded):
            None    
        if (was.HasLastGameEnded   != instance.HasLastGameEnded):
            if instance.HasLastGameEnded==True:
                #end_of_week()
                #handling with a cron job for now
                None 
        
    
    
def diff_changes(sender, instance, **kwargs):
# Initially it was my understanding that we'd be communicating real-time changes
# but actually Bill doesn't care about that so much
# so skip this code for now
    return None
    
    player_type = ContentType.objects.get_for_model(PlayerGame)
    team_type   = ContentType.objects.get_for_model(TeamGame)
    my_type   = ContentType.objects.get_for_model(sender)
    
    
    try:
        obj = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        # For now, not sending initial object write changes.  Must consider as we test...
        None
    else:
        saved = model_to_dict(obj) 
        unsaved = model_to_dict(instance) 
        
      
        for key in saved.keys():
            s = saved[key] 
            u = unsaved[key]
            if u is None:
                continue
            
            if type(s) is datetime:
                continue

            # wait what?  Casts u to the same object type as s
            u = type(s)(u) 
                
            if s != u: # Field has changed

                current_week = Thisweek.objects.last().Week
                weeks = (int(current_week), int(current_week)-1)  # Verify this logic...
               
                 
                if(my_type==player_type): 
                    qmodel = Player
                elif(my_type==team_type):
                    qmodel = Team
                    
                """
                Player or defense score changed.  If we picked this player for this week, or for last week, we need to notify...
                Need to decide how to manage past picks...maybe some kind of pick history table
                """
                picks = Pick.objects.filter(threepak__start_week__in=weeks, content_type=ContentType.objects.get_for_model(qmodel))


                if(my_type==player_type): 
                    title = "%s update" % instance.player.Name
                elif(my_type==team_type):
                    title = "%s team defense update" % instance.team.abbr

                was = str(s) 
                now = str(u)
                
                # Note: We can't calculate total scores yet because this score is still in pre-save mode! 
                
                for pp in picks: 
                   
                    try:
                        
                        contests = Contest.objects.filter(threepaks__id=pp.threepak.id)
                        if len(contests):
                            contest = contests.first()
                         
                        c = Context(locals())
                        if(my_type==player_type): 
                            t = get_template('player_changed.txt')
                        elif(my_type==team_type):
                            t = get_template('team_changed.txt')
                        txt = t.render(c)
                    except Exception as ex:
                        print "failed to render"
                        print locals()
                        continue
                    
                    if(my_type==player_type): 
                        cmp = instance.player.PlayerID==pp.content_object.PlayerID
                    else:
                        cmp = instance.team.abbr==pp.content_object.abbr
                          
                    if cmp:
                        print "====="
                        print txt
                        #send_my_mail(title, txt, pp.threepak.user.username)
            
