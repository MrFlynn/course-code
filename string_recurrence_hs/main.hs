import Data.List

-- Recursively generates strings from some base list of a given size.
generateStrings :: Int -> [String] -> [String] -> [String]
generateStrings size bases input = concat (map string_fork bases)
  where
    -- Manages recursive calls. Generates different "forks" in the tree
    -- containing all possible string combinations of the base array.
    string_fork :: String -> [String]
    string_fork str
      | str_len < size  = generateStrings (size - str_len) bases new_array
      | str_len == size = new_array
      | otherwise       = []
        where
           str_len    = length str
           new_array  = map add_new_elem input 
           -- Appends str to all items in input array.
            where
              add_new_elem :: String -> String
              add_new_elem = (str ++)

-- Create comma-separated string from string array.
createCommaSeparatedString :: [String] -> String
createCommaSeparatedString = intercalate ", "

main :: IO()
main = do
  -- Get string length from user.
  putStrLn "Input string length:"
  strsSize <- readLn :: IO Int

  -- Generate all strings using the array below.
  let baseStrings = ["A", "BB", "BC", "CB", "CC", "EEF", "FEE"]
  let allStrings = generateStrings strsSize baseStrings [""]

  -- Output list of strings and the length of the array.
  putStrLn "\nStrings:"
  putStrLn (createCommaSeparatedString allStrings)
  putStrLn ("\nNumber of strings = " ++ show (length allStrings))