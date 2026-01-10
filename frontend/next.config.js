/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Conditionally set basePath and assetPrefix based on environment
  basePath: process.env.NODE_ENV === 'production' ? process.env.NEXT_PUBLIC_BASE_PATH || '' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? process.env.NEXT_PUBLIC_ASSET_PREFIX || '' : '',
}

module.exports = nextConfig