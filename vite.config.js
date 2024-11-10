// vite.config.js
import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';
import fs from 'fs';
import path from 'path';

function debugSymlinks(dir, depth = 0) {
    const indent = '  '.repeat(depth);
    console.log(`${indent}Checking directory: ${dir}`);

    if (!fs.existsSync(dir)) {
        console.warn(`${indent}Directory does not exist: ${dir}`);
        return;
    }

    const entries = fs.readdirSync(dir, { withFileTypes: true });

    entries.forEach(entry => {
        const fullPath = path.join(dir, entry.name);
        console.log(`${indent}- ${entry.name} (${entry.isSymbolicLink() ? 'symlink' : entry.isDirectory() ? 'directory' : 'file'})`);

        if (entry.isSymbolicLink()) {
            try {
                const realPath = fs.realpathSync(fullPath);
                console.log(`${indent}  → points to: ${realPath}`);
                console.log(`${indent}  → target exists: ${fs.existsSync(realPath)}`);
            } catch (error) {
                console.error(`${indent}  → ERROR resolving symlink: ${error.message}`);
            }
        }

        if (entry.isDirectory() && !entry.isSymbolicLink()) {
            debugSymlinks(fullPath, depth + 1);
        }
    });
}

function resolveSymlinks() {
    return {
        name: 'vite-plugin-symlink-resolver',
        enforce: 'pre',
        configResolved(config) {
            // Print build configuration
            console.log('\nVite configuration:');
            console.log('- Root:', config.root);
            console.log('- Base:', config.base);
            console.log('- Build target:', config.build.target);
            console.log('- Outdir:', config.build.outDir);

            // Debug symlinks
            console.log('\nAnalyzing project structure:');
            const staticDir = path.join(process.cwd(), 'static');
            debugSymlinks(staticDir);
        },
        configureServer(server) {
            server.middlewares.use((req, res, next) => {
                if (req.url?.startsWith('/')) {
                    const staticPath = path.join(process.cwd(), 'static');
                    const requestedPath = path.join(staticPath, req.url);

                    try {
                        if (fs.existsSync(requestedPath)) {
                            const realPath = fs.realpathSync(requestedPath);
                            console.log(`Resolved ${req.url} → ${realPath}`);
                            if (fs.existsSync(realPath)) {
                                req.url = '/' + path.relative(staticPath, realPath);
                            }
                        }
                    } catch (error) {
                        console.warn(`Warning handling ${req.url}:`, error.message);
                    }
                }
                next();
            });
        }
    };
}

export default defineConfig({
    plugins: [
        resolveSymlinks(),
        sveltekit()
    ],
    server: {
        fs: {
            allow: [
                // Add the root directory of your project and parent directories of symlink targets
                process.cwd(),
                '/Users/daniel.ellis/WIPwork/CMIP6Plus_CVs'
            ]
        }
    },
    build: {
        rollupOptions: {
            onwarn(warning, warn) {
                // Log detailed warning information
                console.log('\nRollup warning:', warning);
                warn(warning);
            }
        }
    }
});

// You might also need a static file copy script
// // copy-static.js
// import fs from 'fs';
// import path from 'path';

function ensureDirectoryExists(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

function copyWithSymlinks(src, dest) {
    console.log(`Copying from ${src} to ${dest}`);

    ensureDirectoryExists(dest);

    const entries = fs.readdirSync(src, { withFileTypes: true });

    entries.forEach(entry => {
        const srcPath = path.join(src, entry.name);
        const destPath = path.join(dest, entry.name);

        if (entry.isSymbolicLink()) {
            try {
                const realPath = fs.realpathSync(srcPath);
                console.log(`Resolving symlink: ${srcPath} → ${realPath}`);

                if (fs.existsSync(realPath)) {
                    const stats = fs.statSync(realPath);
                    if (stats.isDirectory()) {
                        copyWithSymlinks(realPath, destPath);
                    } else {
                        fs.copyFileSync(realPath, destPath);
                    }
                } else {
                    console.error(`Symlink target does not exist: ${realPath}`);
                }
            } catch (error) {
                console.error(`Error processing symlink ${srcPath}:`, error);
            }
        } else if (entry.isDirectory()) {
            copyWithSymlinks(srcPath, destPath);
        } else {
            fs.copyFileSync(srcPath, destPath);
        }
    });
}

