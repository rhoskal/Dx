import subprocess
import re


def git_diff():
    """ get a list of all files changed on current branch """
    files = subprocess.Popen(["git", "diff", "--name-only", "$(git rev-parse --abbrev-ref HEAD)", "$(git merge-base $(git rev-parse --abbrev-ref HEAD)", "develop"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT
                             )

    return files.communicate()


def get_touched_pkgs(files=[], graph=None):
    if graph == None or files == []:
        return None

    pkgs = set()

    for f in files:
        for pkg in graph:
            if pkg['dir'] in f:
                pkgs.add(pkg['name'])

    return pkgs


if __name__ == "__main__":
    graph = [
      {
        "name": "web",
        "dir": "apps/web",
        "affects": []
      },
      {
        "name": "mobile",
        "dir": "apps/mobile",
        "affects": []
      },
      {
        "name": "chat",
        "dir": "packages/chat",
        "affects": ["web"]
      },
      {
        "name": "components",
        "dir": "packages/components",
        "affects": ["mobile", "web"]
      },
      {
        "name": "logic",
        "dir": "packages/logic",
        "affects": ["mobile", "web", "chat", "components", "ui"]
      },
      {
        "name": "ui",
        "dir": "packages/ui",
        "affects": ["mobile", "web", "chat", "components"]
      }
    ];

    files = b'apps/mobile/src/profile/RequestSessionModalView.js\napps/web/src/components/Forms/FormikFormInput.js\napps/web/src/sessions/SessionRequest.js\napps/web/src/sessions/SessionRequest.spec.js\napps/web/src/sessions/__snapshots__/SessionRequest.spec.js.snap\napps/web/src/sessions/components/ContactCard.js\napps/web/src/sessions/components/__snapshots__/ContactCard.spec.js.snap\napps/web/src/sessions/forms/SessionRequestForm.js\napps/web/src/sessions/modals/AddInviteeModal.js\napps/web/src/sessions/modals/PermissionsModal.js\napps/web/src/sessions/routes.js\npackages/ui/src/components/Incrementor.jsx\npackages/ui/src/components/Incrementor.spec.jsx\npackages/ui/src/components/SegmentedControl.jsx\npackages/ui/src/components/SegmentedControl.spec.jsx\npackages/ui/src/components/TouchableBox.jsx\npackages/ui/src/components/__snapshots__/Incrementor.spec.jsx.snap\npackages/ui/src/components/index.js\npackages/ui/src/stories/SegmentedControl.stories.jsx'

    touched = get_touched_pkgs(files.split('\n'), graph)

    if touched == None:
        exit(1)
    else:
        affected = set()
        for t in touched:
            for pkg in graph:
                if t == pkg['name']:
                    affected.add(pkg['name'])
                    for p in pkg['affects']:
                        affected.add(p)

        # print('yarn lerna run test:ci --scope ' + ','.join(affected))
        print(','.join(affected))
