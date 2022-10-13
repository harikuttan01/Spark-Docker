import scala.collection.JavaConverters._
val s=System.getenv.asScala
for( (key,value) <- s){
println(key,value)
}
