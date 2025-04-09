from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from octofit_tracker.test_data import get_test_data

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activities, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Clear existing data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Get test data
        data = get_test_data()

        # Insert test data
        User.objects.bulk_create([User(**user) for user in data['users']])

        # Insert teams and add members
        teams = []
        for team_data in data['teams']:
            members = team_data.pop('members')  # Extract members
            team = Team.objects.create(**team_data)  # Create team
            member_instances = [User.objects.get(email=member['email']) for member in members]  # Convert to User instances
            team.members.add(*member_instances)  # Add members to the team
            teams.append(team)

        # Convert user field in activities to User instances
        activities = []
        for activity_data in data['activities']:
            user_data = activity_data.pop('user')  # Extract user data
            user_instance = User.objects.get(email=user_data['email'])  # Get User instance
            activity_data['user'] = user_instance  # Replace with User instance
            activities.append(Activity(**activity_data))
        Activity.objects.bulk_create(activities)

        Leaderboard.objects.bulk_create([Leaderboard(**entry) for entry in data['leaderboard']])
        Workout.objects.bulk_create([Workout(**workout) for workout in data['workouts']])

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
