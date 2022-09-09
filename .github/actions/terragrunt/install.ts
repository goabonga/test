import * as path from 'path';
import * as core from '@actions/core';
import * as tc from '@actions/tool-cache';
import * as exec from '@actions/exec';
import * as httpm from '@actions/http-client';
import { ExecOptions } from '@actions/exec/lib/interfaces';
import { IS_WINDOWS, IS_LINUX, getDownloadFileName } from './utils';
import { Octokit } from "@octokit/core";

const TOKEN = core.getInput('token');
const AUTH = !TOKEN ? undefined : `token ${TOKEN}`;
const REPO_OWNER = 'gruntwork-io';
const REPO_NAME = 'terragrunt';

export async function findRelease(
  semanticVersionSpec: string,
  architecture: string,
  releases: any[] | null
): Promise<any | undefined> {
  if (!releases) {
    releases = await getReleases();
  }

  // Assuming tc.findFromManifest can be adapted or another filtering method is used
  const foundRelease = releases.find(release => release.tag_name.includes(semanticVersionSpec) && release.assets.some(asset => asset.name.includes(architecture)));

  return foundRelease;
}

export async function getReleases(): Promise<any[]> {
  try {
    return await getReleasesFromRepo();
  } catch (err) {
    core.debug('Fetching the releases via the API failed.');
    if (err instanceof Error) {
      core.debug(err.message);
    }
  }
  return await getReleasesFromURL();
}

export async function getReleasesFromRepo(): Promise<any[]> {
  core.debug(
    `Getting releases from ${REPO_OWNER}/${REPO_NAME}`
  );

  const octokit = new Octokit({ auth: TOKEN });

  const response = await octokit.request('GET /repos/{owner}/{repo}/releases', {
    owner: REPO_OWNER,
    repo: REPO_NAME,
    headers: {
      'X-GitHub-Api-Version': '2022-11-28'
    }
  });

  if (response.status !== 200) {
    throw new Error(`Unable to get releases from GitHub repository ${REPO_OWNER}/${REPO_NAME}`);
  }

  return response.data;
}

export async function getReleasesFromURL(): Promise<any[]> {
  core.debug('Falling back to fetching the releases using raw URL.');

  const http: httpm.HttpClient = new httpm.HttpClient('tool-cache');
  const response = await http.getJson<any[]>(`https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases`);
  if (!response.result) {
    throw new Error(`Unable to get releases from ${REPO_OWNER}/${REPO_NAME}`);
  }
  return response.result;
}

async function installTerragrunt(workingDirectory: string) {
  const options: ExecOptions = {
    cwd: workingDirectory,
    env: {
      ...process.env,
      ...(IS_LINUX && { LD_LIBRARY_PATH: path.join(workingDirectory, 'lib') })
    },
    silent: true,
    listeners: {
      stdout: (data: Buffer) => {
        core.info(data.toString().trim());
      },
      stderr: (data: Buffer) => {
        core.error(data.toString().trim());
      }
    }
  };

  if (IS_WINDOWS) {
    await exec.exec('powershell', ['./setup.ps1'], options);
  } else {
    await exec.exec('bash', ['./setup.sh'], options);
  }
}

export async function installTerragruntFromRelease(release: any) {
  const asset = release.assets.find((asset: any) => {
    if (IS_WINDOWS) {
      return asset.name.includes('windows') && asset.name.endsWith('.exe');
    } else if (IS_LINUX) {
      return asset.name.includes('linux');
    } else {
      return asset.name.includes('darwin');
    }
  });

  if (!asset) {
    throw new Error('No suitable asset found for the current platform.');
  }

  const downloadUrl = asset.browser_download_url;

  core.info(`Download from "${downloadUrl}"`);
  let terragruntPath = '';
  try {
    const fileName = getDownloadFileName(downloadUrl);
    terragruntPath = await tc.downloadTool(downloadUrl, fileName, AUTH);
    core.info('Extract downloaded archive');
    let terragruntExtractedFolder;
    if (IS_WINDOWS) {
      terragruntExtractedFolder = await tc.extractZip(terragruntPath);
    } else {
      terragruntExtractedFolder = await tc.extractTar(terragruntPath);
    }

    core.info('Execute installation script');
    await installTerragrunt(terragruntExtractedFolder);
  } catch (err) {
    if (err instanceof tc.HTTPError) {
      // Rate limit?
      if (err.httpStatusCode === 403 || err.httpStatusCode === 429) {
        core.info(
          `Received HTTP status code ${err.httpStatusCode}.  This usually indicates the rate limit has been exceeded`
        );
      } else {
        core.info(err.message);
      }
      if (err.stack) {
        core.debug(err.stack);
      }
    }
    throw err;
  }
}
