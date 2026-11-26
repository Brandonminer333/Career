# Career

This repo acts as a hub for my career experience to be tracked, documented, and made available to the world. I develop my GitHub Profile README.md and GitHub Pages here in one single repo and rely on GitHub Actions to push changes outward to `Brandonminer333/Brandonminer333` and `Brandonminer333/Brandonminer333.github.io`.

The reason for this setup is that I am in the process of organizing my resume information and all other relevant information into a single `config.json` file. The idea is that I'll be able to enter new information into the config file and have my portfolio and GitHub profile update automatically and stay i sync with each other.

## Build Tools

### Portfolio

I am using Astro because I need to keep the site in pure HTML and static, but pure HTML and CSS is clunky and scales horribly. I knew I needed an SSG, and decided to go with Astro because it relied on basically pure HTML and CSS — unlike Jekyll with Ruby — and has a bit more popularity and info online.

 I really like SSGs, and would recommend anyone with programming experience who is learning HTML to consider trying it out as it resolves — at least for me — the clunkiness of raw HTML by allowing building with reusable templates/layouts and components. If you couldn't tell, I come from a Machine learning background, very much not frontend.

### Profile

I am using a custom python script to build the `README.md` file from scratch inside of a GitHub Action. This is the most simple solution since I only need to worry about a single file, so managing it entirely in a python script is not impossible.