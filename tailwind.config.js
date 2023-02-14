/** @type {import('tailwindcss').Config} */

module.exports = {
  content: [
      './DjangoBlog/templates/**/*.html',
      './DjangoBlog/blog/templates/**/*.html',
      './node_modules/flowbite/**/*.js'
  ],
  theme: {
    extend: {},
  },
    plugins: [
        require('flowbite/plugin')
  ]
}