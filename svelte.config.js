import adapter from '@sveltejs/adapter-static';

export default {
	kit: {
		adapter: adapter({
			// appDir: './src',
			pages: 'docs',
			assets: 'docs',
			fallback: "src/404.html",
			precompress: false,
			strict: true,
			prerender: {
				entries: [
					'/',  // Home page
					'/activity/lesfmip',  // Pre-rendered activity page
					'/activity/another-activity'  // Another pre-rendered activity page
				]
			}
		}),
		appDir:"src",
		files: {
			assets: 'data_descriptors',  // Directory for static assets
			routes: 'routes',  // Directory for routes
			// template: 'app.html'  // Main HTML template
		},

		// version: "v6.5.0",
	}
};
