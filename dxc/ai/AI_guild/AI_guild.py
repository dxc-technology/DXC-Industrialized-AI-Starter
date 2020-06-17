import json
import requests
from enum import Enum

class AI_Guild_Role(Enum):
    PROJECT_MANAGER = 1,
    DATA_SCIENTIST = 2,
    DATA_ENGINEER = 3,
    ALL = 4

class AI_Badge(Enum):
    CREATE_DATA_STORIES = 1
    RUN_AGILE_TRANSFORMATION = 2
    BUILD_DATA_PIPELINES = 3
    RUN_AI_EXPERIMENT = 4
    BUILD_UTILITY_AI_SERVICES = 5
    PERFORM_AI_FORENSICS = 6
    TEST = 7


def guild_member_should_apply_for_badge(guild_member_roles, ai_badge):


    guild_role_badges = {
        AI_Guild_Role.PROJECT_MANAGER : [AI_Badge.CREATE_DATA_STORIES, AI_Badge.RUN_AGILE_TRANSFORMATION],
        AI_Guild_Role.DATA_SCIENTIST : [AI_Badge.RUN_AI_EXPERIMENT, AI_Badge.PERFORM_AI_FORENSICS],
        AI_Guild_Role.DATA_ENGINEER : [AI_Badge.BUILD_DATA_PIPELINES, AI_Badge.BUILD_UTILITY_AI_SERVICES],
        AI_Guild_Role.ALL: [AI_Badge.CREATE_DATA_STORIES, AI_Badge.RUN_AGILE_TRANSFORMATION, AI_Badge.BUILD_DATA_PIPELINES, AI_Badge.RUN_AI_EXPERIMENT,            AI_Badge.BUILD_UTILITY_AI_SERVICES, AI_Badge.PERFORM_AI_FORENSICS]
        }

    ai_badge_id = {
        AI_Badge.CREATE_DATA_STORIES: "dd05bbdf-ad5b-469d-ab2c-4dd218fd68fe",
        AI_Badge.RUN_AGILE_TRANSFORMATION: "8ec48861-c355-4e44-b98f-0a80cf1440a8",
        AI_Badge.BUILD_DATA_PIPELINES: "2cffc101-8fc3-4680-a8cd-29ec58483832",
        AI_Badge.RUN_AI_EXPERIMENT: "ddeb2020-1db5-48c6-8b2c-ea2e50f050d7",
        AI_Badge.BUILD_UTILITY_AI_SERVICES: "6e8b661f-31bc-46f7-89e4-194e7e6ebb21",
        AI_Badge.PERFORM_AI_FORENSICS: "ec96e016-9e33-4b4e-a6bd-43491e811179",
        AI_Badge.TEST: "b828e318-8501-434e-9f55-ccdb7000ee09"
    }
    #start by assuming we should not apply for the badge
    apply_for_badge = False
    for role in guild_member_roles:
        #apply for the badge if a matching role is found
        if ai_badge in guild_role_badges[role]: apply_for_badge = True
    return apply_for_badge

def apply_for_an_ai_badge(ai_guild_profile, ai_badge):

    guild_role_badges = {
        AI_Guild_Role.PROJECT_MANAGER : [AI_Badge.CREATE_DATA_STORIES, AI_Badge.RUN_AGILE_TRANSFORMATION],
        AI_Guild_Role.DATA_SCIENTIST : [AI_Badge.RUN_AI_EXPERIMENT, AI_Badge.PERFORM_AI_FORENSICS],
        AI_Guild_Role.DATA_ENGINEER : [AI_Badge.BUILD_DATA_PIPELINES, AI_Badge.BUILD_UTILITY_AI_SERVICES],
        AI_Guild_Role.ALL: [AI_Badge.CREATE_DATA_STORIES, AI_Badge.RUN_AGILE_TRANSFORMATION, AI_Badge.BUILD_DATA_PIPELINES, AI_Badge.RUN_AI_EXPERIMENT,            AI_Badge.BUILD_UTILITY_AI_SERVICES, AI_Badge.PERFORM_AI_FORENSICS]
    }

    ai_badge_id = {
        AI_Badge.CREATE_DATA_STORIES: "dd05bbdf-ad5b-469d-ab2c-4dd218fd68fe",
        AI_Badge.RUN_AGILE_TRANSFORMATION: "8ec48861-c355-4e44-b98f-0a80cf1440a8",
        AI_Badge.BUILD_DATA_PIPELINES: "2cffc101-8fc3-4680-a8cd-29ec58483832",
        AI_Badge.RUN_AI_EXPERIMENT: "ddeb2020-1db5-48c6-8b2c-ea2e50f050d7",
        AI_Badge.BUILD_UTILITY_AI_SERVICES: "6e8b661f-31bc-46f7-89e4-194e7e6ebb21",
        AI_Badge.PERFORM_AI_FORENSICS: "ec96e016-9e33-4b4e-a6bd-43491e811179",
        AI_Badge.TEST: "b828e318-8501-434e-9f55-ccdb7000ee09"
    }
    
    # Construct apiEndponit string
    apiPath = f'badges/{ai_badge_id[ai_badge]}/assertions'
    apiEndpoint = f'{ai_guild_profile["badge_platform_apiHost"]}{ai_guild_profile["badge_platform_apiBasePath"]}{apiPath}'  

    headers = {
        'Content-Type': 'application/json',
        'X-Api-Key': ai_guild_profile["badge_platform_apiKey"]
    }

    #for each member in the guild:
    num_guild_members = len(ai_guild_profile['guild_members'])
    for i in range(1,num_guild_members + 1):
    #apply for the badge if applicable
        if guild_member_should_apply_for_badge(ai_guild_profile['guild_members'][i]['roles'], ai_badge):
            payload = {
            'email': ai_guild_profile['guild_members'][i]['badge_applicant_email'],
            'evidence': ai_guild_profile["badge_evidence"]
            }
            response = requests.post(
                apiEndpoint,
                headers=headers,
                json=payload
            )
  
            print(response)
            print(json.dumps(response.json(), indent=4))
