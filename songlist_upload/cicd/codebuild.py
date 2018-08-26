from troposphere import Ref, Template, Output, GetAtt, Join, Sub, Parameter
from troposphere.iam import Role, PolicyType
from troposphere.codebuild import Project, Artifacts, Environment, Source, SourceAuth
from awacs.aws import Action, Allow, Policy, Statement

# NOTE: Before this can be created, authorize Region specific CodeBuild OAUTH access in GitHub
# https://docs.aws.amazon.com/codebuild/latest/APIReference/API_ProjectSource.html#CodeBuild-Type-ProjectSource-location

t = Template()

t.add_description("Packages and publishes the code for the lambda function that updates"
                  "the song list when csv is uploaded to s3")

cloudformation_s3_bucket_name = 'smyleeface-public'
project_name = 'jukebox_alexa'
codebuild_service_name = 'JukeboxAlexa-SonglistUpload'
CodeBuildProject = 'CodeBuildProject'

##############################
# Stack parameters
#############################
codebuild_artifact_name = Parameter(
    "ArtifactName",
    Description="filename for the artifact",
    Type="String"
)
t.add_parameter(codebuild_artifact_name)

codebuild_ecr_contianer = Parameter(
    "EcrPythonContainerPath",
    Description="path to the container where the buildspec will run",
    Type="String"
)
t.add_parameter(codebuild_ecr_contianer)

##############################
# Role songlist_upload
#############################
CodeBuildServiceRoleSonglistUpload = 'CodeBuildServiceRoleSonglistUpload'
service_role_name = 'cicd-codebuild-jukebox-songlist-upload-service-role'
codebuild_assume_role_policy = {
    'Version': '2012-10-17',
    'Statement': [
        {
            'Sid': 'listobjectslambda',
            'Effect': 'Allow',
            'Principal': {
                'Service': ['codebuild.amazonaws.com']
            },
            'Action': 'sts:AssumeRole'
        }
    ]
}
t.add_resource(Role(
    title=CodeBuildServiceRoleSonglistUpload,
    RoleName=service_role_name,
    AssumeRolePolicyDocument=codebuild_assume_role_policy
))


cloudformation_title = 'CodeBuildServicePolicySonglistUpload'
policy_name = 'cicd-codebuild-jukebox-songlist-upload-policy'
t.add_resource(PolicyType(
    title=cloudformation_title,
    PolicyDocument=Policy(
        Statement=[
            Statement(
                Effect=Allow,
                Resource=[
                    Join('', ["arn:aws:logs:", Sub('${AWS::Region}'), ':', Sub('${AWS::AccountId}'), ':log-group:/aws/codebuild/', Ref(CodeBuildProject)]),
                    Join('', ["arn:aws:logs:", Sub('${AWS::Region}'), ':', Sub('${AWS::AccountId}'), ':log-group:/aws/codebuild/', Ref(CodeBuildProject), ':*']),
                ],
                Action=[
                    Action('logs', 'CreateLogGroup'),
                    Action('logs', 'CreateLogStream'),
                    Action('logs', 'PutLogEvents')
                ]
            ),
            Statement(
                Effect=Allow,
                Resource=[
                    f'arn:aws:s3:::{cloudformation_s3_bucket_name}/*'
                ],
                Action=[
                    Action('s3', 'PutObject')
                ]
            )
        ],
        Version='2012-10-17'
    ),
    PolicyName=policy_name,
    Roles=[Ref(CodeBuildServiceRoleSonglistUpload)]
))

################
# CodeBuild
################
codebuild_artifact_path = 'songlist_upload/CodeBuildArtifacts'
codebuild_build_spec_path = 'songlist_upload/cicd/buildspec.yaml'
codebuild_github_url = 'https://github.com/smyleeface/jukebox_alexa'
t.add_resource(Project(
    title=CodeBuildProject,
    Name=codebuild_service_name,
    Artifacts=Artifacts(
        Type='NO_ARTIFACTS'
    ),
    BadgeEnabled=True,
    Description='Tests and deploys songlist_upload',
    Environment=Environment(
        ComputeType='BUILD_GENERAL1_SMALL',
        Image=Ref(codebuild_ecr_contianer),
        Type='LINUX_CONTAINER'
    ),
    ServiceRole=Ref(CodeBuildServiceRoleSonglistUpload),
    Source=Source(
        Auth=SourceAuth(
            Resource='GITHUB',
            Type='OAUTH'
        ),
        BuildSpec=codebuild_build_spec_path,
        Location=codebuild_github_url,
        Type='GITHUB'
    )
))


t.add_output([
    Output(
        "CodeBuildServiceRoleSonglistUploadName",
        Description="The name of the service role",
        Value=Ref(CodeBuildServiceRoleSonglistUpload)
    ),
    Output(
        'CodeBuildServiceRoleSonglistUploadArn',
        Description='The ARN of the service role',
        Value=GetAtt(CodeBuildServiceRoleSonglistUpload, 'Arn')
    ),
    Output(
        'CodeBuildProjectId',
        Description='CodeBuildProject Id',
        Value=Ref(CodeBuildProject)
    ),
    Output(
        'CodeBuildProjectArn',
        Description='CodeBuildProject Arn',
        Value=GetAtt(CodeBuildProject, 'Arn')
    )
])

print(t.to_yaml())
