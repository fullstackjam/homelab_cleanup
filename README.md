# Homelab Cleanup
The scripts in this repository are used to clear out existing Cloudflare DNS records, Cloudflare Tunnels, ZeroTier Networks, and Terraform Workspaces to make way for a fresh build process of the [Khuedoan Homelab](https://github.com/khuedoan/homelab).

Since Homelab requires python, I built this to use python scripts. However, the main script to control all the scripts is in bash.

To get started, clone this repo to your controller which is most likely in Ubuntu or Fedora.

Run the following command from within the repo folder:

```bash cleanup.sh```


Disclaimer: This is still a work in progress and has only been tested in my own environment.
