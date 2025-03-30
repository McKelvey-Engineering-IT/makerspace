/**
 * Evaluates if a user is a member based on their membership years and selected year
 * @param {string[]} userYears - Array of years the user has been a member
 * @param {string} selectedYear - Currently selected year to check against ('all' or specific year)
 * @returns {boolean} - Whether the user is a member for the selected year
 */
export const isMemberForYear = (userYears, selectedYear) => {
  if (!Array.isArray(userYears)) return false;
  if (selectedYear === 'all') return userYears.length > 0;
  return userYears.includes(selectedYear);
};