from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from app.models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    customer = serializers.SerializerMethodField()

    def create(self, validated_data):
        user = User.objects.create(
                username=validated_data['username'],
                email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'password', 'first_name', 'last_name', 'customer')

    def get_customer(self, obj):
        customer = obj.profile.customer.name if obj.profile.customer else 'app'
        return customer


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        #lookup_field = 'name'
        #extra_kwargs = {
        #    'url': {'lookup_field': 'name'}
        #}
        fields = '__all__'

class TeamMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMLB
        fields = '__all__'


class StadiumMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = StadiumMLB
        fields = '__all__'


class GameMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameMLB
        fields = '__all__'


class PlayerMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerMLB
        fields = '__all__'


class PlayerGameMLBSerializer(serializers.ModelSerializer):    
    def get_photo_url(self, obj):
        return PlayerMLB.objects.get(PlayerID=obj.PlayerID).PhotoUrl

    def get_status(self, obj):
        return PlayerMLB.objects.get(PlayerID=obj.PlayerID).Status

    PhotoUrl = serializers.SerializerMethodField('get_photo_url')
    Status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = PlayerGameMLB
        fields = ('locked', 'id', 'PlayerID', 'Name', 'Position', 'Team', 'Opponent', 
                  'PhotoUrl', 'Status', 'FantasyPointsFanDuel', 'FanDuelSalary', 'HomeOrAway')        


class TeamGameMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamGameMLB
        fields = '__all__'


class PlayerSeasonMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSeasonMLB
        fields = '__all__'


class TeamSeasonMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamSeasonMLB
        fields = '__all__'


class NewsMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsMLB
        fields = '__all__'


class PlayerGameProjectionMLBSerializer(serializers.ModelSerializer):
    def get_photo_url(self, obj):
        return PlayerMLB.objects.get(PlayerID=obj.PlayerID).PhotoUrl

    def get_status(self, obj):
        return PlayerMLB.objects.get(PlayerID=obj.PlayerID).Status

    PhotoUrl = serializers.SerializerMethodField('get_photo_url')
    Status = serializers.SerializerMethodField('get_status')

    class Meta:
        model = PlayerGameProjectionMLB
        fields = ('locked', 'id', 'PlayerID', 'Name', 'Position', 'Team', 
                  'Opponent', 'PhotoUrl', 'Status', 'FantasyPointsFanDuel', 'FanDuelSalary', 'HomeOrAway')        



class PlayerSeasonProjectionMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSeasonProjectionMLB
        fields = '__all__'


class StandingMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = StandingMLB
        fields = '__all__'


class DfsSlatePlayerMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = DfsSlatePlayerMLB
        fields = '__all__'


class DfsSlateGameMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = DfsSlateGameMLB
        fields = '__all__'


class DfsSlateMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = DfsSlateMLB
        fields = '__all__'


class InningMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = InningMLB
        fields = '__all__'


class BoxScoreMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxScoreMLB
        fields = '__all__'


class ScheduleMLBSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleMLB
        fields = '__all__'


class TournamentSpecSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TournamentSpec
        fields = ('id', 'description', 'max_players', 'guaranteed_payout', 'friendly_name', 'cost')

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News 
        fields = '__all__' 

class TournamentPlacementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TournamentPlacement
        fields = ('id', 'place', 'pays', 'spec',)


class StripeTokenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StripeToken
        fields = ('user', 'token')


class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ('vs', 'Date', 'GameKey')


class ContentObjectSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PlayerGameMLB
        fields = ('id',)


class ThreePakSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ThreePak
        fields = ('id',)


class PickSerializer(serializers.HyperlinkedModelSerializer):
    content_object = ContentObjectSerializer()
    threepak = ThreePakSerializer()

    class Meta:
        model = Pick
        fields = ('id', 'session_week', 'content_object', 'threepak')


class CustomAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"))
    customer = serializers.CharField(label=_("Play"), required=False)
    password = serializers.CharField(label=_("Password"), style={'input_type': 'password'})

    class Meta:
        fields = '__all__'
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        customer = attrs.get('customer')
        if not customer:
            customer = getattr(settings, 'PAK_DEFAULT_CUSTOMERPROFILE', 'app')
        try:
            CustomerProfile.objects.get(name=customer)
        except:
            msg = _('Matching Customer Profile: [{}] not found.'.format(customer))
            raise serializers.ValidationError(msg)

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.profile.customer and customer != 'app':
                    msg = _('Your account is linked with a different company game. '
                            'Create a new account or log into your "{}" account at '
                            'https://apps.3pak.com/?play={}'.format('app','app'))
                    raise serializers.ValidationError(msg)
                elif user.profile.customer and user.profile.customer.name != customer:
                    msg = _('Your account is linked with a different company game. '
                            'Create a new account or log into your "{}" account at '
                            'https://apps.3pak.com/?play={}'.format(user.profile.customer, user.profile.customer))
                    raise serializers.ValidationError(msg)
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs
