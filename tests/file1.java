/**
 * 
 */
package projectone;

import static org.junit.Assert.*;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Ignore;
import org.junit.Test;

/**
 * @author nicky
 *
 */
public class TestA {

    /**
     * @throws java.lang.Exception
     */
    @BeforeClass
    public static void setUpBeforeClass() throws Exception {
    }

    /**
     * @throws java.lang.Exception
     */
    @AfterClass
    public static void tearDownAfterClass() throws Exception {
    }

    /**
     * @throws java.lang.Exception
     */
    @Before
    public void setUp() throws Exception {
    }

    /**
     * @throws java.lang.Exception
     */
    @After
    public void tearDown() throws Exception {
    }

    @Test
    public void test() {
        fail("Not yet implemented");
    }
    
    // REQ: as
    @Test   
    public void testOne(){
        fail("Not yet implemented");    
    }
    

    // REQ: 1, 2, 3, 4, 5
    @Ignore
    @Test
    public void testTwo(){
        fail("Not yet implemented");    
    }    

    // REQ: 1, 2, 3, 4, 5, 6
    @Ignore
    @Test   
    public void testThree(){
        fail("Not yet implemented");    
    }        
}
