import { Given, When, Then } from '@cucumber/cucumber';
import { render, screen } from '@testing-library/react';
import App from '../App';

Given('the App is loaded', () => {
  render(<App />);
});

When('I look at the header', () => {
  // This step might not need code if just viewing the component
});

Then('I should see a button with text {string}', (buttonText) => {
  expect(screen.getByText(buttonText)).toBeInTheDocument();
});
Then('I should see a word with text {string}', (buttonText) => {
  expect(screen.getByText(buttonText)).toBeInTheDocument();
});