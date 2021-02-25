#! /usr/bin/env python

import os.path
import jira
import argparse
import json
import pprint

'''
Module to allow for scripting of Jira ticket creation.  The template can be as
small or as large as you desire, but the simplest includes a summary and a
description.
'''

def main():
    '''
    Main program
    '''
    parser = argparse.ArgumentParser(
        description='Create a JIRA ticket',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-S', '--server', help='The JIRA server url', default='https://bnrobotics.atlassian.net')
    parser.add_argument('-p', '--password', help='The JIRA password for <user>.  Normal password does not'
                        'seem to work, but an APIToken seems to work just fine')
    parser.add_argument('-u', '--user', help='The JIRA user name, typically your email address')
    parser.add_argument('-P', '--project', help='The project name/key/id under which to create the ticket')
    parser.add_argument('-i', '--issue', help='The issue name/key/id to create the ticket', default='Task')
    parser.add_argument('-s', '--start', help='The robot number to start with', type=int)
    parser.add_argument('-e', '--end', help='The robot number to end on', type=int)
    parser.add_argument('-b', '--batchsize', help='Batch size of ticket create calls', type=int, default=10)
    parser.add_argument('-d', '--dryrun',
                        help='Do not actually execute the comand to create tickets, but do everything else',
                        default=False, action='store_true')
    parser.add_argument('-r', '--robotbase', help='The base name to use for the robot name, i.e. atlasoscar',
                        default='')
    parser.add_argument('-t', '--template', help='''The json teamplate of the ticket, something like:
{
    'summary': 'Create keys for %ROBOT%',
    'description': 'Longer text that describes the steps needed to handle the request'
}

Project and issuetype information will be added.
%ROBOT% will be replaces with the full robot name
%ROBOTNUM% will be replaced with the robot number
    ''')
    args = parser.parse_args()

    jiraconn = jira.JIRA(args.server, basic_auth=(args.user, args.password))
    projects = jiraconn.projects()
    # Locate the project
    project = [x for x in projects if x.key == args.project or x.name == args.project or x.id == args.project]
    assert project, 'Could not find a project matching %s' % args.project
    project = project[0]
    issuetypes = jiraconn.issue_types()
    validissues = [x for x in issuetypes if not hasattr(x, 'scope') or x.scope.project.id == project.id]
    issue = [x for x in validissues if x.name == args.issue or x.id == args.issue]
    assert issue, 'Could not find an issue matching %s' % args.issue
    issue = issue[0]

    tickettemplate = json.load(open(args.template))

    ticketlist = []
    for robotnum in range(args.start, args.end+1):
        robot = '%s%d' % (args.robotbase, robotnum)
        currentticket = dict()
        currentticket.update(tickettemplate)
        for key, value in currentticket.items():
            if '%ROBOT%' in value or '%ROBOTNUM%' in value:
                currentticket[key] = value.replace('%ROBOT%', robot).replace('%ROBOTNUM%', str(robotnum))
        currentticket.update(
            dict(
                project=dict(key=project.key),
                issuetype=dict(name=issue.name)
            )
        )
        ticketlist.append(currentticket)

    if args.dryrun:
        for tstart in range(0, len(ticketlist)+1, args.batchsize):
            pprint.pprint(ticketlist[tstart:tstart+args.batchsize])
    else:
        for tstart in range(0, len(ticketlist)+1, args.batchsize):
            issues = jiraconn.create_issues(field_list=ticketlist[tstart:tstart+args.batchsize])
            for issue in issues:
                print 'Created %s' % issue

if __name__ == '__main__':
    main()
