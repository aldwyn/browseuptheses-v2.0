<?php

    include('app/connectToServer.php');
 
    $terms = array(); 
    $maximum = 0; 
     
    $query = mysql_query("SELECT category_name, counter FROM category ORDER BY counter DESC LIMIT 30");
     
    while ($row = mysql_fetch_array($query)) {
        $term = $row['category_name'];
        $counter = $row['counter'];
     
        if ($counter > $maximum) {
            $maximum = $counter;
        }
     
        $terms[] = array('term' => $term, 'counter' => $counter);
     
    }

    shuffle($terms);

?>

<!DOCTYPE html>
<html>
    <head>
        <title>Tag Cloud Example</title>
        <style type="text/css">
            #tagcloud {
                width: 100%;
                min-height: 150px;  
                background: white;
                color:#0066FF;
                padding: 10px;
                border: 1px solid #559DFF;
                text-align:center;
                -moz-border-radius: 4px;
                -webkit-border-radius: 4px;
                border-radius: 5px;
                font-family: 'Segoe UI Semilight';
                margin-bottom: 20px;
            }

            #tagcloud a:link, #tagcloud a:visited {
                text-decoration:none;
                color: #333;
            }

            #tagcloud a:hover {
                text-decoration: underline;
            }

            #tagcloud span {
                padding: 4px;
            }

            #tagcloud .smallest {
                font-size: 25px;
            }

            #tagcloud .small {
                font-size: 30px;
            }

            #tagcloud .medium {
                font-size: 35px;
            }

            #tagcloud .large {
                font-size: 40px;
            }

            #tagcloud .largest {
                font-weight: bold;
                font-size: 40px;
            }
        </style>
    </head>

    <body>
        <!-- <h1>Search</h1>
        <form id="search" method="get" action="?action=search">
            <input type="text" name="term" id="term" />
            <input type="submit" name="submit" id="submit" value="Search" />
        </form> -->
        
        <div id="tagcloud">
            <?php 
            foreach ($terms as $term):
                $percent = floor(($term['counter'] / $maximum) * 100);

                if ($percent < 10):
                    $class = 'smallest';
                elseif ($percent >= 10 and $percent < 30):
                    $class = 'small';
                elseif ($percent >= 30 and $percent < 50):
                    $class = 'medium';
                elseif ($percent >= 50 and $percent < 70):
                    $class = 'large';
                else:
                    $class = 'largest';
                endif;
            ?>
            <span class="<?php echo $class; ?>">
                <a href="search.php?search=<?php echo urlencode($term['term']); ?>&category=All"><?php echo $term['term']; ?></a>
            </span>
            <?php endforeach; ?>
        </div>
    </body>
</html>