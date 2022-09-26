import argparse

from kubernetes import config
from kubernetes.client import Configuration
from kubernetes.client.api import core_v1_api
from kubernetes.client.rest import ApiException
from kubernetes.stream import stream


def exec_commands(api_instance, args):

    resp = None

    pod_name = args.pod
    namespace = args.namespace

    try:
        resp = api_instance.read_namespaced_pod(name=pod_name,
                                                namespace=namespace)
    except ApiException as e:
        if e.status != 404:
            print("Unknown error: %s" % e)
            exit(1)

    if not resp:
        print("Pod %s does not exist, exiting." % pod_name)
        exit(1)

    exec_command = [
        '/bin/sh',
        '-c',
        'echo Hello from pod $HOSTNAME']

    resp = stream(api_instance.connect_get_namespaced_pod_exec,
                  pod_name,
                  namespace,
                  command=exec_command,
                  stderr=True, stdin=False,
                  stdout=True, tty=False)

    print(resp)

def main():

    parser = argparse.ArgumentParser(description="Pod exec")
    parser.add_argument("--pod", type=str, help="name of pod to exec", default="busybox")
    parser.add_argument("--namespace", type=str, help="namespace of pod", default="default")

    args = parser.parse_args()

    config.load_kube_config()
    try:
        c = Configuration().get_default_copy()
    except AttributeError:
        c = Configuration()
        c.assert_hostname = False
    Configuration.set_default(c)
    core_v1 = core_v1_api.CoreV1Api()

    exec_commands(core_v1, args)


if __name__ == '__main__':
    main()