import datetime
import gzip
import optparse
import os
import jinja2

template = jinja2.Template("""
.TH {{ name.upper() }} {{ section }} "{{ date.strftime("%B, %d %Y") }}"
.SH NAME
{{ name }} - {{ short_description }}
.SH SYNOPSIS
.PP
.B {{ name }}{% if synposis_list %}
{{ '\n'.join(synposis_list) }}{% endif %}
.SH DESCRIPTION
.PP
{{ long_description }}{% if option_list %}
.SH OPTIONS
{% for option in option_list %}.TP
.B {{ option.flags }}
{{ option.description }}{% endfor %}{% endif %}
.SH "AUTHOR"
.PP
This stub was created by Silas Sewell for the Fedora Project.
{% if see_also %}.SH "SEE ALSO"
{{ see_also }}{% endif %}
""".lstrip())

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_man(**kwargs):
    kwargs['date'] = datetime.datetime.now()
    f = None
    try:
        dir_path = os.path.join(kwargs['options'].mandir, 'man%s' % kwargs['section'])
        create_dir(dir_path)
        man_path = os.path.join(dir_path, '%s.%s.gz' % (kwargs['name'], kwargs['section']))
        f = gzip.open(man_path, 'wb')
        f.write(template.render(**kwargs))
    finally:
        if f is not None:
            f.close()

def main(options):
    def create(**kwargs):
        kwargs['options'] = options
        create_man(**kwargs)
    create(
        name='st',
        section=8,
        short_description='manage swift containers',
        long_description='Perform operations on swift containers such a stat, list, upload, download and delete.',
        synposis_list=[
            '[options]',
            '[command]',
            '[args]',
        ],
        option_list=[
            {'flags': '-h, --help', 'description': 'show help information'},
        ],
        see_also='',
    )
    create(
        name='swift-account-audit',
        section=8,
        short_description='manually audit swift accounts',
        long_description='Manually checks the integrity of swift accounts.',
        synposis_list=[
            '[options]',
            '[url 1]',
            '[url 2]',
        ],
        option_list=[
            {'flags': '-c [concurrency]', 'description': 'Set the concurrency, default 50'},
            {'flags': '-r [ring dir]', 'description': 'Ring locations, default /etc/swift'},
            {'flags': '-e [filename]', 'description': 'File for writing a list of inconsistent urls'},
            {'flags': '-d', 'description': 'Also download files and verify md5'},
        ],
        see_also='swift-account-auditor(8)',
    )
    create(
        name='swift-account-auditor',
        section=8,
        short_description='daemon that audits swift accounts',
        long_description='Daemon that checks the integrity of accounts.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='swift-account-audit(8)',
    )
    create(
        name='swift-account-reaper',
        section=8,
        short_description='daemon that removes data from deleted swift accounts',
        long_description='Removes data from status=DELETED accounts. The account is not deleted immediately by the services call, but instead the account is simply marked for deletion by setting the status column in the account_stat table of the account database. This account reaper scans for such accounts and removes the data in the background. The background deletion process will occur on the primary account server for the account.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-account-replicator',
        section=8,
        short_description='daemon that replicates swift accounts',
        long_description='Replicate account data to other servers.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-account-server',
        section=8,
        short_description='daemon that serves swift account data',
        long_description='Daemon that exposes swift account data via a RESTful interface.',
        synposis_list=[
            'CONFIG_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-auth-create-account',
        section=8,
        short_description='create swift user account',
        long_description='Creates swift user accounts.',
        synposis_list=[
            '<new_account>',
            '<new_user>',
            '<new_password>',
            '[conf_file]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-auth-recreate-accounts',
        section=8,
        short_description='re-create user accounts',
        long_description='Re-creates the accounts from the existing auth database in the swift cluster.',
        synposis_list=[
            'CONFIG_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-auth-server',
        section=8,
        short_description='swift user account daemon',
        long_description='Daemon that serves and manages user accounts.',
        synposis_list=[
            'CONFIG_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-container-auditor',
        section=8,
        short_description='daemon that audits swift containers',
        long_description='Daemon that checks the integrity of containers.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-container-replicator',
        section=8,
        short_description='daemon that replicates swift containers',
        long_description='Replicate container data to other servers.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-container-server',
        section=8,
        short_description='daemon that lists the content of containers',
        long_description='The Container Server\'s primary job is to handle listings of objects. It doesn\'t know where those object\'s are, just what objects are in a specific container.',
        synposis_list=[
            'CONFIG_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-container-updater',
        section=8,
        short_description='daemon that updates container information',
        long_description='The Container Updater updates information in account listings.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-drive-audit',
        section=8,
        short_description='update drive information',
        long_description='Update drive information.',
        synposis_list=[
            'CONFIG_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-get-nodes',
        section=8,
        short_description='show responsible node',
        long_description='Shows the nodes responsible for the item specified.',
        synposis_list=[
            '<ring.gz>',
            '<account>',
            '[<container>]',
            '[<object>]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-init',
        section=8,
        short_description='manage swift servers',
        long_description='Start, stop and reload swift servers.',
        synposis_list=[
            '<server-name>',
            '[start|stop|reload]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-object-auditor',
        short_description='daemon that audits swift objects',
        long_description='Daemon that checks the integrity of objects.',
        section=8,
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-object-info',
        section=8,
        short_description='display object info',
        long_description='Display information about an object such as account, container, hash and content type.',
        synposis_list=[
            'OBJECT_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-object-replicator',
        section=8,
        short_description='daemon that replicates swift objects',
        long_description='Replicate object data to other servers.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-object-server',
        section=8,
        short_description='daemon that serves objects',
        long_description='Daemon that exposes swift object data via a RESTful interface.',
        synposis_list=[
            'CONFIG_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-object-updater',
        section=8,
        short_description='update object information in container listings',
        long_description='Object Updater updates object information in container listings.',
        synposis_list=[
            'CONFIG_FILE',
            '[once]',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-proxy-server',
        section=8,
        short_description='centralize swift daemon',
        long_description='The Proxy Server is responsible for tying the other servers together. For each request, it will look up the location of the account, container, or object in the ring and route the request accordingly. The public API is also exposed through the Proxy Server.',
        synposis_list=[
            'CONFIG_FILE',
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-ring-builder',
        section=8,
        short_description='assigns partitions to devices and writes ring structure',
        long_description='The ring-builder assigns partitions to devices and writes an optimized Python ring structure to a gzipped, pickled file on disk for shipping out to the servers.',
        synposis_list=[
        ],
        option_list=[
        ],
        see_also='',
    )
    create(
        name='swift-stats-populate',
        section=8,
        short_description='run dispersion and performance population',
        long_description='Run dispersion and performance population.',
        synposis_list=[
        ],
        option_list=[
            {'flags': '-h, --help', 'description': 'show help information'},
        ],
        see_also='',
    )
    create(
        name='swift-stats-report',
        section=8,
        short_description='run various swift reports',
        long_description='Run swift reports such as audit checks, dispersion reports and performance reports.',
        synposis_list=[],
        option_list=[
            {'flags': '-h, --help', 'description': 'show help information'},
        ],
        see_also='',
    )

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option(
        '--mandir',
        dest='mandir',
        help='use PATH as base mandir',
        metavar='PATH',
        default='.',
    )
    options, args = parser.parse_args()
    main(options)
