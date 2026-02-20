---
name: together-code-sandbox
description: Spin up full VM sandboxes with Docker support via Together Code Sandbox (powered by CodeSandbox). Sizes from Pico (2 CPU, 1GB) to XLarge (64 CPU, 128GB). Memory snapshots, sub-3-second cloning, browser connectivity. Use when users need full VM environments, Docker containers, dev servers, persistent sandboxes, or compute environments beyond simple Python execution.
---

# Together Code Sandbox

## Overview

Full VM sandboxes with Docker support, memory snapshots, and sub-3-second cloning. Powered by CodeSandbox infrastructure.

- SDK: `npm install @codesandbox/sdk`
- Auth: CodeSandbox API token from https://codesandbox.io/t/api
- Features: Docker/Dev Containers, filesystem persistence, browser connectivity

## Quick Start

```typescript
import { CodeSandbox } from "@codesandbox/sdk";

const sdk = new CodeSandbox(process.env.CSB_API_KEY!);

// Create a sandbox
const sandbox = await sdk.sandboxes.create();
const session = await sandbox.connect();

// Run commands
const output = await session.commands.run("echo 'Hello World'");
console.log(output); // Hello World
```

## Sandbox Lifecycle

| Bootup Type | Description |
|-------------|-------------|
| `FORK` | Created from a template (snapshot clone) |
| `RUNNING` | Already running (on resume) |
| `RESUME` | Resumed from hibernation |
| `CLEAN` | Fresh start (no snapshot available) |

## Templates

Create custom templates with pre-configured environments:

```shell
npx @codesandbox/sdk build ./my-template --ports 5173
```

Use templates when creating sandboxes:
```typescript
const sandbox = await sdk.sandboxes.create({
  source: 'template',
  id: 'my-template-tag',
});
```

## Browser Connectivity

Connect sandboxes to browser sessions:

```typescript
// Server-side
const session = await sandbox.createBrowserSession({ id: req.session.username });

// Client-side
import { connectToSandbox } from '@codesandbox/sdk/browser';
const sandbox = await connectToSandbox({
  session: initialSessionFromServer,
  getSession: (id) => fetchJson(`/api/sandboxes/${id}`),
});
await sandbox.fs.writeTextFile('test.txt', 'Hello World');
```

## VM Sizes & Pricing

| VM Size | CPU | RAM | Cost/hour |
|---------|-----|-----|-----------|
| Pico | 2 cores | 1 GB | $0.074 |
| Nano | 2 cores | 4 GB | $0.149 |
| Micro | 4 cores | 8 GB | $0.297 |
| Small | 8 cores | 16 GB | $0.594 |
| Medium | 16 cores | 32 GB | $1.189 |
| Large | 32 cores | 64 GB | $2.378 |
| XLarge | 64 cores | 128 GB | $4.755 |

Default recommendation: Nano for most workloads, Pico for simple code execution.

## Concurrent VM Plans

- **Build (free)**: 10 concurrent VMs
- **Scale**: 250 concurrent VMs ($170/mo base)
- **Enterprise**: Custom limits and credit discounts

## Key Features

- **Memory snapshots**: Checkpoint and restore VM state
- **Sub-3s cloning**: Fork from templates instantly
- **Docker support**: Full Dev Container spec support
- **FS persistence**: Git version control on VM filesystem
- **Auto-hibernate**: Sandboxes hibernate when disconnected
