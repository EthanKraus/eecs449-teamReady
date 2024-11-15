## Introduction

This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

## Getting Started

1. Download the npm package installer using the following command:   
`npm install`  

2. Run npm install axios to download the axios package:     
`npm install axios`

3. Download the proper python packages using pip by running the following command:  
`pip install -r requirements.txt`

4. Create a .env.local file and store the following information:
```  
NEXT_PUBLIC_API_URL=https://api.openai.com/v1/chat/completions    
NEXT_PUBLIC_API_KEY=[FILL IN WITH OPENAI KEY] 
NEXT_PUBLIC_MODEL=gpt-3.5-turbo
```   

5. To get your secret OpenAI key, go to the website https://platform.openai.com/api-keys and create a  
secret key, then paste this value into the corresponding blank in your created .env.local file

6. Now, you can run the following command to run the project:     
`npm run dev`

7. Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
