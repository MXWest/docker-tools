import docker
from docker.errors import APIError
from src import perror

client = docker.from_env()


def cleanup_untagged_images():
    """
    :return: list of containers that prevented an image from being removed
    """
    blocking_containers = []
    for image in client.images.list():
        if not image.attrs["RepoTags"]:
            try:
                client.images.remove(image.short_id)
                print("Removed image {0}".format(image.short_id))
            except APIError as e:
                container = e.explanation.split()[-1]
                perror(
                    "Unable to remove image {0}: still in use by {1}".format(
                        image.short_id, container
                    )
                )
                blocking_containers.append(container)
        else:
            print("Keeping {0}".format(image.attrs["RepoTags"][0]))
    return blocking_containers


def cleanup_blocking_containers(containers):
    """
    :param containers: list of containers to try to remove
    :return: list of containers we were able to remove
    """
    for cid in containers:
        removed_containers = []
        c = client.containers.get(cid)
        try:
            c.remove()
            removed_containers.append(cid)
            print("Removed container {0}".format(c))
        except APIError as e:
            perror("Unable to remove container {0]: {1}".format(cid, e.explanation))

        return removed_containers


if __name__ == "__main__":
    cleanup_blocking_containers(cleanup_untagged_images()) and print(
        "{0}".format(cleanup_untagged_images())
    )
