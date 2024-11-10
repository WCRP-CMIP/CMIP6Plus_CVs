// svelte.config.js
import adapter from '@sveltejs/adapter-static';
// import { vitePreprocess } from '@sveltejs/kit/vite';

import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';
/** @type {import('@sveltejs/kit').Config} */
const config = {
	kit: {
		adapter: adapter({
			pages: 'docs',
			assets: 'docs',
			fallback: undefined,
			precompress: false,
			strict: false // only for testing, make this true in prod
		}),
		prerender: {
			handleMissingId: 'warn',
			entries: ['*']
		},
		files:{
			assets: 'data_descriptors'
		}
	},
	preprocess: vitePreprocess()
};

export default config;

// import adapter from '@sveltejs/adapter-static';

// export default {
// 	kit: {
// 		adapter: adapter({
// 			// appDir: './src',
// 			pages: 'docs',
// 			assets: 'docs',
// 			fallback: "src/404.html",
// 			precompress: false,
// 			strict: false,
// 			prerender: {
// 				entries: [
// 					'/activity/lesfmip',
// 					'/activity/cmip',
// 				]
// 			}
// 		}),
// 		appDir:"src",
// 		files: {
// 			assets: 'data_descriptors',  // Directory for static assets
// 			routes: 'routes',  // Directory for routes
// 			// template: 'app.html'  // Main HTML template
// 		},
// 		// version: "v6.5.0",
// 	}
// };
// //entries
// 			// '/',  // Home page
// 					// '/activity/lesfmip',  // Pre-rendered activity page
// 					// '/activity/another-activity'  // Another pre-rendered activity page
