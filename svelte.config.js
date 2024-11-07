import adapter from '@sveltejs/adapter-static';

export default {
	kit: {
		adapter: adapter({
			// default options are shown. On some platforms
			// these options are set automatically — see below
			appDir: 'src',
			pages: 'docs',
			assets: 'docs',
			fallback: "404.html",
			precompress: false,
			strict: true
		})
	}
};
