export default {
  testEnvironment: 'jsdom',
  transform: {
    '^.+\\.(ts|tsx)$': 'babel-jest', // Transformar arquivos .ts e .tsx
    '^.+\\.(js|jsx)$': 'babel-jest' // Transformar arquivos .js e .jsx
  },
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx'],
  moduleNameMapper: {
    '\\.(css|less)$': '<rootDir>/src/__mocks__/styleMock.js',
  },
};
